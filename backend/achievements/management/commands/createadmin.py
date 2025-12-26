from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Create superuser from environment variables (DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD). Safe to run multiple times.'

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_true', help='Run without interactive prompts')

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(self.style.NOTICE('DJANGO_SUPERUSER_* env vars not set; skipping createadmin.'))
            return

        from django.contrib.auth import get_user_model
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.NOTICE(f"Superuser '{username}' already exists; skipping."))
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'. Please remove DJANGO_SUPERUSER_* vars from environment."))
        except Exception as e:
            self.stderr.write(str(e))
            raise

