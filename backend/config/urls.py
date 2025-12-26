from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponseBadRequest
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/achievements/', include('achievements.urls')),
    path('api/content/', include('content.urls')),
]

# Temporary protected endpoint to create superuser when console is not available.
# To use: set ADMIN_SETUP_TOKEN env in Railway to a long random string, redeploy,
# then call: curl "https://<your-backend>/internal-create-admin/?token=<that-token>". Remove endpoint and token after use.

def _internal_create_admin(request):
    token = request.GET.get('token')
    secret = os.environ.get('ADMIN_SETUP_TOKEN')
    if not secret:
        return HttpResponseBadRequest('ADMIN_SETUP_TOKEN not set on server')
    if token != secret:
        return HttpResponseBadRequest('invalid token')

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    if not username or not email or not password:
        return HttpResponseBadRequest('DJANGO_SUPERUSER_* env vars missing')

    from django.contrib.auth import get_user_model
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'exists', 'username': username})
    User.objects.create_superuser(username=username, email=email, password=password)
    return JsonResponse({'status': 'created', 'username': username})

# register route only when DEBUG is False to avoid accidental exposure in development
if not settings.DEBUG:
    urlpatterns += [
        path('internal-create-admin/', _internal_create_admin),
    ]

# Для отображения медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)