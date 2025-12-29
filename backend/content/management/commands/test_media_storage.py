from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import uuid

class Command(BaseCommand):
    help = 'Save a small test file through default_storage to verify where media uploads go (S3 vs local). Use --cleanup to remove the file after test.'

    def add_arguments(self, parser):
        parser.add_argument('--cleanup', action='store_true', help='Delete the test file after creation')

    def handle(self, *args, **options):
        name = f'test_media_check/{uuid.uuid4().hex}.txt'
        content = ContentFile(b'Test file for media storage check')
        self.stdout.write(f'DEFAULT_FILE_STORAGE = {getattr(settings, "DEFAULT_FILE_STORAGE", None)}')
        try:
            saved_name = default_storage.save(name, content)
            url = default_storage.url(saved_name)
            self.stdout.write(self.style.SUCCESS(f'Saved test file as: {saved_name}'))
            self.stdout.write(self.style.SUCCESS(f'Accessible at URL: {url}'))
            self.stdout.write(self.style.SUCCESS(f'Storage class: {default_storage.__class__.__module__}.{default_storage.__class__.__name__}'))
            if options.get('cleanup'):
                try:
                    default_storage.delete(saved_name)
                    self.stdout.write(self.style.SUCCESS('Deleted test file (cleanup=true)'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Failed to delete test file: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to save test file: {e}'))
            raise

