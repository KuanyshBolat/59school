from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Print MEDIA_URL and storage settings (for debugging)'

    def handle(self, *args, **options):
        self.stdout.write(f"MEDIA_URL={getattr(settings, 'MEDIA_URL', None)}")
        self.stdout.write(f"DEFAULT_FILE_STORAGE={getattr(settings, 'DEFAULT_FILE_STORAGE', None)}")
        self.stdout.write(f"AWS_STORAGE_BUCKET_NAME={getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)}")
        self.stdout.write(f"AWS_S3_CUSTOM_DOMAIN={getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)}")

