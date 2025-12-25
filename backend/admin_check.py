import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from django.apps import apps
from django.contrib import admin

out = {}

out['db_name'] = str(settings.DATABASES['default']['NAME'])
out['db_abspath'] = os.path.abspath(str(settings.DATABASES['default']['NAME']))
out['media_root'] = settings.MEDIA_ROOT

# list installed apps
out['installed_apps'] = list(settings.INSTALLED_APPS)

# admin registered models
out['admin_registered'] = [m._meta.label for m in admin.site._registry.keys()]

# model counts for achievements.Certificate and content models
counts = {}
try:
    Certificate = apps.get_model('achievements', 'Certificate')
    counts['achievements.Certificate'] = Certificate.objects.count()
except LookupError:
    counts['achievements.Certificate'] = 'model not found'

content_models = {}
for model_name in ['NavLink','Header','HeroSlide','About','Stat','Director','ContactInfo','Footer','Page','ImageBlock']:
    try:
        m = apps.get_model('content', model_name)
        content_models[model_name] = m.objects.count()
    except LookupError:
        content_models[model_name] = 'model not found'

out['content_counts'] = content_models
out['counts'] = counts

# sample rows (titles/images) for HeroSlide and Certificate
samples = {}
try:
    HeroSlide = apps.get_model('content', 'HeroSlide')
    samples['hero_samples'] = list(HeroSlide.objects.all().values('id','title','image')[:10])
except LookupError:
    samples['hero_samples'] = []

try:
    Certificate = apps.get_model('achievements','Certificate')
    samples['certificate_samples'] = list(Certificate.objects.all().values('id','title','image')[:10])
except LookupError:
    samples['certificate_samples'] = []

out['samples'] = samples

# write to file
with open('admin_dump.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('Wrote admin_dump.json')

