from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Placeholder createadmin command (no-op). Previously used to create superuser from env; now disabled. Remove this file if not needed.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('createadmin command is disabled.'))
