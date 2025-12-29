from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
import os
import subprocess

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/achievements/', include('achievements.urls')),
    path('api/content/', include('content.urls')),
]


# Temporary protected endpoint to create superuser when console is not available.
# To use: set ADMIN_SETUP_TOKEN env in Railway to a long random string, redeploy,
# then call: curl "https://<your-backend>/internal-create-admin/?token=<that-token>" or
# curl -H "X-Admin-Token: <that-token>" https://<your-backend>/internal-create-admin/
# Remove endpoint and token after use.

def _normalize_token_candidate(token_raw):
    if not token_raw:
        return ''
    # Accept token in query param or header; allow URL-encoding
    try:
        return os.path.normpath(token_raw)
    except Exception:
        return token_raw


def _internal_create_admin(request):
    token_expected = os.environ.get('ADMIN_SETUP_TOKEN')
    token_given = request.GET.get('token') or request.headers.get('X-Admin-Token')
    token_given = _normalize_token_candidate(token_given)
    if not token_expected or token_given != token_expected:
        return HttpResponseBadRequest('invalid token')

    # Create superuser from env vars if present
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    if not username or not password:
        return HttpResponseBadRequest('missing creds')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'already_exists'})
    User.objects.create_superuser(username=username, email=email or '', password=password)
    return JsonResponse({'status': 'created'})


def _internal_upload_media(request):
    token_expected = os.environ.get('ADMIN_SETUP_TOKEN')
    token_given = request.GET.get('token') or request.headers.get('X-Admin-Token')
    token_given = _normalize_token_candidate(token_given)
    if not token_expected or token_given != token_expected:
        return HttpResponseBadRequest('invalid token')

    # Run the management command upload_media_to_s3
    try:
        # Use subprocess to call manage.py so that Django env is same
        base_dir = settings.BASE_DIR
        manage_py = os.path.join(base_dir, 'manage.py')
        subprocess.check_output(['python', manage_py, 'upload_media_to_s3'], stderr=subprocess.STDOUT)
        return JsonResponse({'status': 'uploaded'})
    except subprocess.CalledProcessError as e:
        return HttpResponseBadRequest(str(e.output))


# register routes only when DEBUG is False to avoid accidental exposure in development
if not settings.DEBUG:
    urlpatterns += [
        path('internal-create-admin/', _internal_create_admin),
        path('internal-upload-media/', _internal_upload_media),
    ]

# Для отображения медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)