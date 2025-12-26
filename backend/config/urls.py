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
]

# Для отображения медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)