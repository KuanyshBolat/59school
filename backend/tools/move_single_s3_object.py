"""
Copy a single S3 object to a new key and optionally delete the source.
Usage:
# set env vars or pass --bucket/--region
$env:AWS_ACCESS_KEY_ID="..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_S3_REGION_NAME="eu-north-1"
py backend\tools\move_single_s3_object.py --src "1.jpg" --dst "student/1.jpg" --dry-run
py backend\tools\move_single_s3_object.py --src "1.jpg" --dst "student/1.jpg" --apply --force

Behavior:
- Checks that source exists.
- If destination exists and --force not set, aborts (no overwrite).
- Copies object without ACL (compatible with BucketOwnerEnforced).
- If --apply specified, deletes source after successful copy.
"""
import os
import sys
import argparse
import boto3
from botocore.exceptions import ClientError


def head_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        code = e.response.get('Error', {}).get('Code', '')
        if code in ('404', 'NotFound'):
            return False
        return False


def copy_object(s3, bucket, src, dst):
    try:
        s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': src}, Key=dst)
        return True, None
    except ClientError as e:
        return False, e


def delete_object(s3, bucket, key):
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        return True, None
    except ClientError as e:
        return False, e


def main():
    parser = argparse.ArgumentParser(description='Copy single S3 object to new key and optionally delete source')
    parser.add_argument('--src', required=True, help='Source key (e.g. 1.jpg)')
    parser.add_argument('--dst', required=True, help='Destination key (e.g. student/1.jpg)')
    parser.add_argument('--bucket', default=os.environ.get('AWS_STORAGE_BUCKET_NAME'), help='Bucket name or set AWS_STORAGE_BUCKET_NAME')
    parser.add_argument('--region', default=os.environ.get('AWS_S3_REGION_NAME') or os.environ.get('AWS_REGION'), help='AWS region')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without performing')
    parser.add_argument('--apply', action='store_true', help='Perform copy and optional delete (requires --apply)')
    parser.add_argument('--force', action='store_true', help='Overwrite destination if exists')
    parser.add_argument('--keep-src', action='store_true', help='Do not delete source even when --apply')
    args = parser.parse_args()

    if not args.bucket:
        print('ERROR: bucket not specified (use --bucket or set AWS_STORAGE_BUCKET_NAME)')
        sys.exit(2)

    session = boto3.session.Session(region_name=args.region)
    s3 = session.client('s3')

    src = args.src
    dst = args.dst
    bucket = args.bucket

    print(f'Bucket: {bucket}  Region: {args.region}')
    print(f'Source: {src}')
    print(f'Destination: {dst}')

    src_exists = head_exists(s3, bucket, src)
    if not src_exists:
        print('ERROR: source does not exist in bucket')
        sys.exit(3)

    dst_exists = head_exists(s3, bucket, dst)
    if dst_exists and not args.force:
        print('ERROR: destination already exists. Use --force to overwrite.')
        sys.exit(4)

    if args.dry_run:
        print('DRY-RUN: would copy source -> dest' + (', then delete source' if args.apply and not args.keep_src else ''))
        sys.exit(0)

    # perform copy
    ok, err = copy_object(s3, bucket, src, dst)
    if not ok:
        print(f'ERROR copying: {err}')
        sys.exit(5)
    print('Copied successfully')

    if args.apply and not args.keep_src:
        ok_del, err_del = delete_object(s3, bucket, src)
        if not ok_del:
            print(f'ERROR deleting source: {err_del}')
            sys.exit(6)
        print('Deleted source')

    print('Done')

if __name__ == '__main__':
    main()

