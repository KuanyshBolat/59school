from rest_framework import serializers
from .models import (
    NavLink, Header, HeroSlide, About, Stat, Director, ContactInfo, Footer, Page, ImageBlock
)

class NavLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavLink
        fields = ['id', 'name', 'href', 'order']

class HeaderSerializer(serializers.ModelSerializer):
    nav_links = NavLinkSerializer(many=True)
    class Meta:
        model = Header
        fields = ['id', 'logo', 'phone', 'email', 'nav_links']

class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = ['id', 'title', 'subtitle', 'image', 'order']

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'body', 'image', 'title_color', 'body_color']

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'number', 'label', 'order']

class DirectorSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = ImageBlock
        fields = ['id', 'image', 'caption', 'alt', 'order']

class PageSerializer(serializers.ModelSerializer):
    images = ImageBlockSerializer(many=True, read_only=True)
    class Meta:
        model = Page
        fields = ['id', 'slug', 'title', 'body', 'order', 'images']
