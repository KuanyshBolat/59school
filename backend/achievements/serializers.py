from rest_framework import serializers
from django.conf import settings
from .models import Certificate


def _build_image_url(obj, field_name):
    try:
        field = getattr(obj, field_name)
    except Exception:
        return ''
    if not field:
        return ''
    try:
        url = field.url
        if url:
            return url
    except Exception:
        pass
    name = getattr(field, 'name', None) or str(field)
    if not name:
        return ''
    custom = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    if custom:
        return f'https://{custom.rstrip("/")}/{name.lstrip("/")}'
    media = getattr(settings, 'MEDIA_URL', None) or '/media/'
    if media.startswith('http'):
        return f"{media.rstrip('/')}/{name.lstrip('/')}"
    return f"{media.rstrip('/')}/{name.lstrip('/')}"


class CertificateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _build_image_url(obj, 'image')

    class Meta:
        model = Certificate
        fields = ['id', 'title', 'year', 'image', 'category', 'level', 'order']