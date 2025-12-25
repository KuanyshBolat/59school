from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from django import forms
from .models import (
    NavLink, Header, HeroSlide, About, Stat, Director, ContactInfo, Footer, Page, ImageBlock
)

class ImageBlockInline(admin.TabularInline):
    model = ImageBlock
    extra = 1

class HeroSlideAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" style="height:80px; object-fit:cover;" />', obj.image.url)
            except Exception:
                return obj.image
        return '-'
    image_tag.short_description = 'Preview'

    list_display = ('id', 'title', 'subtitle', 'order', 'image_tag')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'subtitle')
    readonly_fields = ('image_tag',)

class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'label', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('label',)

class NavLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'href', 'order')
    ordering = ('order',)
    search_fields = ('name', 'href')

class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email')
    filter_horizontal = ('nav_links',)
    search_fields = ('phone', 'email')

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageBlockInline]
    search_fields = ('title', 'slug')
    ordering = ('order',)

class AboutAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" style="height:80px; object-fit:cover;" />', obj.image.url)
            except Exception:
                return obj.image
        return '-'
    image_tag.short_description = 'Preview'

    list_display = ('id', 'title', 'image_tag', 'title_color', 'body_color')
    search_fields = ('title', 'body')
    readonly_fields = ('image_tag',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 60})},
    }

class DirectorAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" style="height:80px; object-fit:cover; border-radius:50%;" />', obj.image.url)
            except Exception:
                return obj.image
        return '-'
    image_tag.short_description = 'Photo'

    list_display = ('id', 'name', 'title', 'image_tag', 'name_color', 'bio_color')
    search_fields = ('name', 'bio')
    readonly_fields = ('image_tag',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 60})},
    }

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'phone', 'email', 'text_color')
    search_fields = ('address', 'phone', 'email')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 60})},
    }

class FooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title', 'body')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 60})},
    }

# Color picker forms
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'title_color': forms.TextInput(attrs={'type': 'color'}),
            'body_color': forms.TextInput(attrs={'type': 'color'}),
        }

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'
        widgets = {
            'name_color': forms.TextInput(attrs={'type': 'color'}),
            'bio_color': forms.TextInput(attrs={'type': 'color'}),
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'
        widgets = {
            'text_color': forms.TextInput(attrs={'type': 'color'}),
        }

# Assign forms to admin classes
AboutAdmin.form = AboutForm
DirectorAdmin.form = DirectorForm
ContactInfoAdmin.form = ContactInfoForm

# Register models with explicit admin classes
admin.site.unregister(NavLink) if NavLink in admin.site._registry else None
admin.site.unregister(Header) if Header in admin.site._registry else None
admin.site.unregister(HeroSlide) if HeroSlide in admin.site._registry else None
admin.site.unregister(About) if About in admin.site._registry else None
admin.site.unregister(Stat) if Stat in admin.site._registry else None
admin.site.unregister(Director) if Director in admin.site._registry else None
admin.site.unregister(ContactInfo) if ContactInfo in admin.site._registry else None
admin.site.unregister(Footer) if Footer in admin.site._registry else None
admin.site.unregister(Page) if Page in admin.site._registry else None

admin.site.register(NavLink, NavLinkAdmin)
admin.site.register(Header, HeaderAdmin)
admin.site.register(HeroSlide, HeroSlideAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(Page, PageAdmin)
