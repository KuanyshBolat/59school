import os
import boto3
from django.core.management.base import BaseCommand
from django.conf import settings

# This command uploads selected static images from front/public into the configured S3 bucket
# It mirrors the folder layout used by `import_static_content` generation: hero/, about/, director/

FRONT_PUBLIC = os.path.join(settings.BASE_DIR, '..', '..', 'front', 'public')

FILES_MAP = {
    'hero': ['modern-school-students.jpg', 'students-learning-in-classroom-together.jpg', 'diverse-students-teamwork-achievement.jpg'],
    'about': ['123.JPG'],
    'director': ['school-director-professional-portrait.jpg']
}

class Command(BaseCommand):
    help = 'Upload selected media files from front/public to configured S3 bucket (used in production)'

    def handle(self, *args, **options):
        if not os.path.exists(FRONT_PUBLIC):
            self.stderr.write(self.style.ERROR(f'front/public not found at expected path: {FRONT_PUBLIC}'))
            return

        bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        if not bucket:
            self.stderr.write(self.style.ERROR('AWS_STORAGE_BUCKET_NAME not set in environment.'))
            return

        aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region = os.environ.get('AWS_S3_REGION_NAME') or None

        if not aws_key or not aws_secret:
            self.stderr.write(self.style.ERROR('AWS credentials not found in environment (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY).'))
            return

        session = boto3.session.Session(
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=region
        )
        s3 = session.client('s3')

        uploaded = 0
        for folder, files in FILES_MAP.items():
            for fname in files:
                src = os.path.join(FRONT_PUBLIC, fname)
                if not os.path.exists(src):
                    self.stdout.write(self.style.WARNING(f'File not found, skipping: {src}'))
                    continue

                key = f'{folder}/{fname}'
                try:
                    with open(src, 'rb') as f:
                        s3.put_object(Bucket=bucket, Key=key, Body=f, ACL='public-read', ContentType=self._guess_content_type(fname))
                    self.stdout.write(self.style.SUCCESS(f'Uploaded {src} -> s3://{bucket}/{key}'))
                    uploaded += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Failed to upload {src} -> {key}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Uploaded {uploaded} files.'))

    def _guess_content_type(self, fname: str) -> str:
        if fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg'):
            return 'image/jpeg'
        if fname.lower().endswith('.png'):
            return 'image/png'
        return 'application/octet-stream'

