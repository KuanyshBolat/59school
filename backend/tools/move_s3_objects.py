"""
Move/copy S3 objects from bucket root into folder prefixes (hero/, about/, director/)
Usage (PowerShell):
$env:AWS_ACCESS_KEY_ID="..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_S3_REGION_NAME="eu-north-1"
$env:AWS_STORAGE_BUCKET_NAME="59school-media-123"
py backend\tools\move_s3_objects.py --dry-run
py backend\tools\move_s3_objects.py --apply

Script behavior:
- Scans bucket for objects with no '/' in key (root-level objects).
- If basename matches a known filename (case-insensitive) in FILES_MAP, it will copy the object to prefix/<basename> and, when --apply is used, delete the original object.
- By default runs in dry-run mode printing planned operations.
- Safe: does copy first, then delete only after successful copy.

Note: if filenames on S3 don't match expected basenames, you can modify FILES_MAP to include them or run manual aws s3 mv commands.
"""
import os
import sys
import argparse
import boto3
from botocore.exceptions import ClientError

# Map of target prefix -> list of possible filenames (exact basenames)
FILES_MAP = {
    'hero': ['modern-school-students.jpg', 'students-learning-in-classroom-together.jpg', 'diverse-students-teamwork-achievement.jpg'],
    'about': ['123.JPG', '123.jpg'],
    'director': ['school-director-professional-portrait.jpg']
}

# Flatten mapping for quick lookup (lowercase basename -> prefix)
lookup = {}
for prefix, names in FILES_MAP.items():
    for n in names:
        lookup[n.lower()] = prefix


def iter_root_objects(s3, bucket):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if '/' not in key:
                yield key


def move_object(s3, bucket, key, dest_key):
    copy_source = {'Bucket': bucket, 'Key': key}
    try:
        # copy without ACL to respect BucketOwnerEnforced
        s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=dest_key)
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
    parser = argparse.ArgumentParser(description='Move root S3 objects into folder prefixes according to FILES_MAP')
    parser.add_argument('--apply', action='store_true', help='Perform copy+delete (default is dry-run)')
    parser.add_argument('--bucket', type=str, default=os.environ.get('AWS_STORAGE_BUCKET_NAME'), help='Bucket name (env AWS_STORAGE_BUCKET_NAME)')
    parser.add_argument('--region', type=str, default=os.environ.get('AWS_S3_REGION_NAME') or os.environ.get('AWS_REGION'), help='AWS region')
    args = parser.parse_args()

    if not args.bucket:
        print('ERROR: bucket not specified (pass --bucket or set AWS_STORAGE_BUCKET_NAME)')
        sys.exit(2)

    session = boto3.session.Session(region_name=args.region)
    s3 = session.client('s3')

    root_keys = list(iter_root_objects(s3, args.bucket))
    if not root_keys:
        print('No root-level objects found in bucket')
        return

    planned = []
    for key in root_keys:
        basename = os.path.basename(key)
        prefix = lookup.get(basename.lower())
        if prefix:
            dest_key = f"{prefix}/{basename}"
            planned.append((key, dest_key))
        else:
            # no mapping found
            pass

    if not planned:
        print('No matching root objects to move based on FILES_MAP. Found root keys:')
        for k in root_keys:
            print(' -', k)
        print('\nIf your files have different names, update FILES_MAP in this script or move manually.')
        return

    print('Planned moves:')
    for src, dst in planned:
        print(f'  {src} -> {dst}')

    if not args.apply:
        print('\nDRY-RUN: to perform actions run with --apply')
        return

    # apply changes: copy then delete
    succeeded = []
    failed = []
    for src, dst in planned:
        ok, err = move_object(s3, args.bucket, src, dst)
        if ok:
            print(f'Copied: {src} -> {dst}')
            # delete original
            ok_del, err_del = delete_object(s3, args.bucket, src)
            if ok_del:
                print(f'Deleted original: {src}')
                succeeded.append((src, dst))
            else:
                print(f'ERROR deleting original {src}: {err_del}')
                failed.append((src, dst, f'delete error: {err_del}'))
        else:
            print(f'ERROR copying {src} -> {dst}: {err}')
            failed.append((src, dst, f'copy error: {err}'))

    print('\nSummary:')
    print('  succeeded:', len(succeeded))
    print('  failed   :', len(failed))
    if failed:
        print('Failed entries:')
        for f in failed:
            print(' ', f)

if __name__ == '__main__':
    main()

