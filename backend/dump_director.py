import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from content.models import Director
qs = list(Director.objects.values('id','name','bio','name_color','bio_color'))
with open('director_dump.json','w',encoding='utf-8') as f:
    json.dump(qs,f,ensure_ascii=False,indent=2)
print('WROTE director_dump.json')

