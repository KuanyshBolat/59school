import os
from pathlib import Path
import dj_database_url
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load secrets from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Helper to parse comma-separated env lists safely
def env_list(name, default=''):
    raw = os.environ.get(name, default)
    return [s.strip() for s in raw.split(',') if s and s.strip()]

# Helper to normalize origins: remove path and trailing slash and keep scheme://netloc
def normalize_origin(origin: str) -> str:
    origin = origin.strip()
    # If origin looks like host without scheme, return as-is (for ALLOWED_HOSTS use)
    if origin and not origin.startswith('http'):
        return origin
    try:
        parsed = urlparse(origin)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        pass
    # Fallback: strip trailing slash
    return origin.rstrip('/')

# Hosts
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS') if os.environ.get('ALLOWED_HOSTS') else []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'whitenoise.runserver_nostatic',

    # Local apps
    'achievements',
    'content',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Allow DATABASE_URL override (for Postgres in Railway)
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Use WhiteNoise storage in production
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings (normalize origins to avoid corsheaders.E014 errors)
CORS_ALLOWED_ORIGINS = [normalize_origin(o) for o in env_list('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')]
CSRF_TRUSTED_ORIGINS = [normalize_origin(o) for o in env_list('CSRF_TRUSTED_ORIGINS')]

# In development allow all origins for convenience
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Лёгкое логирование применённых конфигов в продакшне (без секретов)
try:
    if not DEBUG:
        import sys
        print('=== DJANGO STARTUP CONFIG ===', file=sys.stdout)
        print(f"CORS_ALLOWED_ORIGINS={CORS_ALLOWED_ORIGINS}", file=sys.stdout)
        print(f"CSRF_TRUSTED_ORIGINS={CSRF_TRUSTED_ORIGINS}", file=sys.stdout)
        print(f"ALLOWED_HOSTS={ALLOWED_HOSTS}", file=sys.stdout)
        print(f"DEBUG={DEBUG}", file=sys.stdout)
except Exception as _e:
    # Не прерываем стартап приложения, просто проигнорируем ошибки логирования
    pass
