# Explanation:
# Добавляю management command `upload_media_s3` для загрузки папки MEDIA_ROOT в указанный S3 bucket.
# Команда использует boto3 и переменные окружения: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME.
# Опции: --public (делать объекты public-read), --prefix (положить медиа под префиксом в бакете).

import os
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
from botocore.exceptions import ClientError

class Command(BaseCommand):
    help = 'Upload contents of MEDIA_ROOT to S3 bucket specified by AWS_STORAGE_BUCKET_NAME environment variable.'

    def add_arguments(self, parser):
        parser.add_argument('--public', action='store_true', help='Make uploaded objects public (ACL public-read)')
        parser.add_argument('--prefix', type=str, default='', help='Optional prefix inside the bucket (no leading slash)')

    def handle(self, *args, **options):
        bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        if not bucket:
            self.stderr.write(self.style.ERROR('AWS_STORAGE_BUCKET_NAME is not set in environment'))
            return

        region = os.environ.get('AWS_S3_REGION_NAME') or os.environ.get('AWS_DEFAULT_REGION')

        # Create S3 client — boto3 will read credentials from env or IAM role
        s3 = boto3.client('s3', region_name=region) if region else boto3.client('s3')

        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            self.stderr.write(self.style.ERROR(f'MEDIA_ROOT does not exist: {media_root}'))
            return

        prefix = options.get('prefix') or ''
        if prefix.startswith('/'):
            prefix = prefix.lstrip('/')

        make_public = options.get('public', False)

        uploaded = 0
        errors = 0

        for root, dirs, files in os.walk(media_root):
            for fname in files:
                full_path = os.path.join(root, fname)
                # key must be relative path from media_root
                rel_path = os.path.relpath(full_path, media_root).replace('\\', '/')
                key = f"{prefix + '/' if prefix else ''}{rel_path}"
                extra_args = {
                    'CacheControl': 'max-age=86400'
                }
                if make_public:
                    extra_args['ACL'] = 'public-read'

                try:
                    # Use upload_file to stream large files
                    s3.upload_file(full_path, bucket, key, ExtraArgs=extra_args)
                    self.stdout.write(self.style.SUCCESS(f'Uploaded {rel_path} -> s3://{bucket}/{key}'))
                    uploaded += 1
                except ClientError as e:
                    self.stderr.write(self.style.ERROR(f'Failed to upload {rel_path}: {e}'))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f'Upload complete. Uploaded: {uploaded}. Errors: {errors}'))

