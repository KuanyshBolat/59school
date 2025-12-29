from rest_framework import serializers
from django.conf import settings
from .models import (
    NavLink, Header, HeroSlide, About, Stat, Director, ContactInfo, Footer, Page, ImageBlock
)


def _build_image_url(obj, field_name):
    """Return absolute URL for ImageField on obj, with safe fallbacks."""
    try:
        field = getattr(obj, field_name)
    except Exception:
        return ''
    if not field:
        return ''
    # If storage provides .url, use it
    try:
        url = field.url
        if url:
            return url
    except Exception:
        pass
    # Fallback: build from storage name using custom domain or MEDIA_URL
    name = getattr(field, 'name', None) or str(field)
    if not name:
        return ''
    # prefer custom domain (no schema)
    custom = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    if custom:
        return f'https://{custom.rstrip("/")}/{name.lstrip("/")}'
    media = getattr(settings, 'MEDIA_URL', None) or '/media/'
    if media.startswith('http'):
        return f"{media.rstrip('/')}/{name.lstrip('/')}"
    # relative MEDIA_URL
    return f"{media.rstrip('/')}/{name.lstrip('/')}"


class NavLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavLink
        fields = ['id', 'name', 'href', 'order']

class HeaderSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return _build_image_url(obj, 'logo')

    nav_links = NavLinkSerializer(many=True)
    class Meta:
        model = Header
        fields = ['id', 'logo', 'phone', 'email', 'nav_links']

class HeroSlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _build_image_url(obj, 'image')

    class Meta:
        model = HeroSlide
        fields = ['id', 'title', 'subtitle', 'image', 'order']

class AboutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _build_image_url(obj, 'image')

    class Meta:
        model = About
        fields = ['id', 'title', 'body', 'image', 'title_color', 'body_color']

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'number', 'label', 'order']

class DirectorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _build_image_url(obj, 'image')

    class Meta:
        model = Director
        fields = ['id', 'name', 'title', 'bio', 'image', 'name_color', 'bio_color']

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'address', 'phone', 'email', 'map_embed', 'text_color']

class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['id', 'title', 'body', 'links']

class ImageBlockSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _build_image_url(obj, 'image')

    class Meta:
        model = ImageBlock
        fields = ['id', 'image', 'caption', 'alt', 'order']

class PageSerializer(serializers.ModelSerializer):
    images = ImageBlockSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'slug', 'title', 'body', 'order', 'images']
