from django.conf import settings
print('INSTALLED_APPS:')
for a in settings.INSTALLED_APPS:
    print(' -', a)

# Import Django to set up
import importlib
try:
    importlib.import_module('achievements.admin')
    importlib.import_module('content.admin')
except Exception as e:
    print('Error importing admin modules:', e)

from django.contrib import admin
print('\nRegistered models in admin:')
for model in admin.site._registry.keys():
    print(' -', model._meta.label)
print('\nDone')

