from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/achievements/', include('achievements.urls')),
    path('api/content/', include('content.urls')),
    # Health endpoint для отладки (возвращает Origin из запроса)
    path('api/health/', lambda request: JsonResponse({'ok': True, 'origin': request.META.get('HTTP_ORIGIN', '')})),
    # Debug endpoint: показывает текущие конфиги CORS/CSRF/ALLOWED_HOSTS (без секретов). Удалить после отладки.
    path('api/debug-config/', lambda request: JsonResponse({
        'CORS_ALLOWED_ORIGINS': settings.CORS_ALLOWED_ORIGINS,
        'CSRF_TRUSTED_ORIGINS': settings.CSRF_TRUSTED_ORIGINS,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'DEBUG': settings.DEBUG,
    })),
]

# Для отображения медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)