# Upload local front/public directory to S3 bucket.
# Usage (PowerShell):
# Set environment variables first, then run:
#   $env:AWS_ACCESS_KEY_ID="..."
#   $env:AWS_SECRET_ACCESS_KEY="..."
#   $env:AWS_REGION="eu-north-1"
#   python backend/tools/upload_front_to_s3.py

# The script reads AWS env vars and uploads files under front/public preserving relative paths.
# It sets ACL public-read and guesses Content-Type via mimetypes.

import os
import sys
import boto3
import mimetypes
from botocore.exceptions import ClientError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FRONT_PUBLIC = os.path.join(BASE_DIR, 'front', 'public')

if __name__ == '__main__':
    bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_S3_REGION_NAME') or os.environ.get('AWS_REGION')

    if not bucket or not aws_key or not aws_secret:
        print('ERROR: AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment')
        sys.exit(2)

    if not os.path.exists(FRONT_PUBLIC):
        print(f'ERROR: front/public not found at expected path: {FRONT_PUBLIC}')
        sys.exit(2)

    session = boto3.session.Session(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, region_name=region)
    s3 = session.client('s3')

    uploaded = 0
    errors = 0
    for root, dirs, files in os.walk(FRONT_PUBLIC):
        for fname in files:
            local_path = os.path.join(root, fname)
            rel_path = os.path.relpath(local_path, FRONT_PUBLIC).replace('\\', '/')
            key = rel_path
            content_type, _ = mimetypes.guess_type(fname)
            extra_args = {'ACL': 'public-read'}
            if content_type:
                extra_args['ContentType'] = content_type
            try:
                s3.upload_file(local_path, bucket, key, ExtraArgs=extra_args)
                print(f'Uploaded: {local_path} -> s3://{bucket}/{key}')
                uploaded += 1
            except Exception as e:
                # boto3 may wrap errors (S3UploadFailedError) — inspect for AccessControlListNotSupported
                msg = ''
                err_code = ''
                try:
                    # ClientError-like
                    err_code = getattr(e, 'response', {}).get('Error', {}).get('Code', '')
                except Exception:
                    err_code = ''
                if not err_code:
                    try:
                        msg = str(e)
                    except Exception:
                        msg = ''
                if err_code == 'AccessControlListNotSupported' or 'AccessControlListNotSupported' in msg:
                    # retry without ACL
                    try:
                        reduced_args = {k: v for k, v in extra_args.items() if k != 'ACL'}
                        s3.upload_file(local_path, bucket, key, ExtraArgs=reduced_args)
                        print(f'Uploaded (no ACL): {local_path} -> s3://{bucket}/{key}')
                        uploaded += 1
                        continue
                    except Exception as e2:
                        print(f'Failed even without ACL: {local_path} -> {key}: {e2}')
                        errors += 1
                        continue
                # Other error
                print(f'Failed: {local_path} -> {key}: {e}')
                errors += 1

    print(f'Done. Uploaded: {uploaded}. Errors: {errors}')
    if errors:
        sys.exit(1)
    sys.exit(0)

