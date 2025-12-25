import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from content.models import HeroSlide, About, Director, Stat

FRONT_PUBLIC = os.path.join(settings.BASE_DIR, '..', 'front', 'public') if False else os.path.join(settings.BASE_DIR, '..', '..', 'front', 'public')
# The above conditional is to make path resolution robust depending on settings.BASE_DIR

class Command(BaseCommand):
    help = 'Import static content (images and initial models) from front/public into media and create DB records'

    def handle(self, *args, **options):
        # Resolve front public path relative to project root
        project_root = settings.BASE_DIR
        front_public = os.path.normpath(os.path.join(project_root, '..', 'front', 'public'))
        self.stdout.write(f"Looking for front public in: {front_public}")

        if not os.path.exists(front_public):
            self.stdout.write(self.style.ERROR('front/public not found. Please ensure front folder is next to backend.'))
            return

        media_root = settings.MEDIA_ROOT
        self.stdout.write(f"Media root: {media_root}")

        # Ensure folders
        folders = {
            'hero': ['modern-school-students.jpg','students-learning-in-classroom-together.jpg','diverse-students-teamwork-achievement.jpg'],
            'about': ['123.JPG'],
            'director': ['school-director-professional-portrait.jpg']
        }

        for folder, files in folders.items():
            dest_dir = os.path.join(media_root, folder)
            os.makedirs(dest_dir, exist_ok=True)
            for fname in files:
                src = os.path.join(front_public, fname)
                if not os.path.exists(src):
                    # try nested student/ or teacher/ folders
                    alt = os.path.join(front_public, 'student', fname)
                    alt2 = os.path.join(front_public, 'teacher', fname)
                    if os.path.exists(alt):
                        src = alt
                    elif os.path.exists(alt2):
                        src = alt2
                if os.path.exists(src):
                    dst = os.path.join(dest_dir, fname)
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)
                        self.stdout.write(self.style.SUCCESS(f'Copied {src} -> {dst}'))
                    else:
                        self.stdout.write(f'{dst} already exists, skipping copy')
                else:
                    self.stdout.write(self.style.WARNING(f'{src} not found'))

        # Create HeroSlides
        slides = [
            {'image': 'hero/modern-school-students.jpg', 'title': '№59 Мектеп гимназиясына қош келдіңіз', 'subtitle': 'Болашақтың лидерлерін қалыптастыратын білім ордасы', 'order': 1},
            {'image': 'hero/students-learning-in-classroom-together.jpg', 'title': 'Сапалы білім беру', 'subtitle': 'Озық технологиялар мен ынталы мұғалімдерден құралған білім ордасы', 'order': 2},
            {'image': 'hero/diverse-students-teamwork-achievement.jpg', 'title': 'Жетістіктің жолы', 'subtitle': 'әрбір оқушының жеке қабілеті ашылып, жан-жақты дамытылады', 'order': 3},
        ]

        for s in slides:
            if not HeroSlide.objects.filter(title=s['title']).exists():
                HeroSlide.objects.create(title=s['title'], subtitle=s['subtitle'], image=s['image'], order=s['order'])
                self.stdout.write(self.style.SUCCESS(f"Created HeroSlide: {s['title']}"))
            else:
                self.stdout.write(f"HeroSlide '{s['title']}' already exists, skipping")

        # About
        if not About.objects.exists():
            About.objects.create(title='Мектеп туралы', body='№50 мектеп-гимназия – балалардың толыққанды дамуы мен озық білім алуына бағытталған заманауи орталық', image='about/123.JPG')
            self.stdout.write(self.style.SUCCESS('Created About'))
        else:
            self.stdout.write('About already exists, skipping')

        # Director
        if not Director.objects.exists():
            Director.objects.create(name='Асан Ержанұлы', title='Директор', bio='Мектебімізде озық әдіс-тәсілдер қолданылады...', image='director/school-director-professional-portrait.jpg')
            self.stdout.write(self.style.SUCCESS('Created Director'))
        else:
            self.stdout.write('Director already exists, skipping')

        # Stats
        stats = [
            {'number': '1420', 'label': 'Оқушылар', 'order': 1},
            {'number': '104', 'label': 'Мұғалімдер', 'order': 2},
            {'number': '9', 'label': 'Жыл мектепке', 'order': 3},
            {'number': '200+', 'label': 'Жетістіктер', 'order': 4},
        ]
        for st in stats:
            if not Stat.objects.filter(number=st['number'], label=st['label']).exists():
                Stat.objects.create(number=st['number'], label=st['label'], order=st['order'])
                self.stdout.write(self.style.SUCCESS(f"Created Stat: {st['label']}"))
            else:
                self.stdout.write(f"Stat {st['label']} exists, skipping")

        self.stdout.write(self.style.SUCCESS('Import complete'))

