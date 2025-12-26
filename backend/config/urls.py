from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponseBadRequest
import os
import urllib.parse

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
    # Return a set of normalized variants to compare against secret
    variants = set()
    if token_raw is None:
        return variants
    token_raw = token_raw.strip()
    variants.add(token_raw)
    try:
        token_decoded = urllib.parse.unquote(token_raw)
        variants.add(token_decoded)
        variants.add(token_decoded.replace(' ', '+'))
        # also try converting spaces to plus then unquote_plus
        variants.add(urllib.parse.unquote_plus(token_raw))
    except Exception:
        pass
    # also try replacing literal spaces with plus
    variants.add(token_raw.replace(' ', '+'))
    return variants


def _internal_create_admin(request):
    # Token can be passed via query param ?token=... or header X-Admin-Token
    token_q = request.GET.get('token')
    token_h = request.headers.get('X-Admin-Token') if hasattr(request, 'headers') else request.META.get('HTTP_X_ADMIN_TOKEN')
    token_candidate_values = set()
    if token_q:
        token_candidate_values.update(_normalize_token_candidate(token_q))
    if token_h:
        token_candidate_values.update(_normalize_token_candidate(token_h))

    secret = os.environ.get('ADMIN_SETUP_TOKEN')
    if not secret:
        return HttpResponseBadRequest('ADMIN_SETUP_TOKEN not set on server')
    if not token_candidate_values:
        return HttpResponseBadRequest('missing token')

    if secret not in token_candidate_values:
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