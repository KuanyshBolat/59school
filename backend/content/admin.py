from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from django import forms
from django.conf import settings
import os
import uuid
import mimetypes
import boto3
from botocore.exceptions import ClientError
from .models import (
    NavLink, Header, HeroSlide, About, Stat, Director, ContactInfo, Footer, Page, ImageBlock
)


class S3AdminUploadMixin:
    """Mixin for ModelAdmin to upload image fields directly to S3 when files are provided via the admin.
    It checks for AWS env vars and uses boto3 to put_object into the configured bucket.
    Works for model image fields and inline formsets.
    """

    def _get_s3_client(self):
        aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region = os.environ.get('AWS_S3_REGION_NAME') or os.environ.get('AWS_REGION')
        if not aws_key or not aws_secret or not os.environ.get('AWS_STORAGE_BUCKET_NAME'):
            return None
        session = boto3.session.Session(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, region_name=region)
        return session.client('s3')

    def _upload_file_to_s3(self, uploaded_file, key):
        """Upload a file-like object to S3 under given key. Returns True on success."""
        s3 = self._get_s3_client()
        bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        if not s3 or not bucket:
            return False, 'S3 client or bucket not configured'
        # seek to start if possible
        try:
            uploaded_file.seek(0)
        except Exception:
            pass
        content_type = getattr(uploaded_file, 'content_type', mimetypes.guess_type(key)[0] or 'application/octet-stream')
        try:
            s3.put_object(Bucket=bucket, Key=key, Body=uploaded_file.read(), ContentType=content_type)
            return True, None
        except ClientError as e:
            return False, str(e)

    def _compute_field_key(self, obj, field, original_name):
        """Compute destination key: combine upload_to and a safe filename (uuid-prefixed to avoid collisions)."""
        upload_to = field.upload_to
        # resolve callable upload_to
        if callable(upload_to):
            try:
                dest = upload_to(obj, original_name)
            except Exception:
                dest = os.path.join(upload_to, original_name) if isinstance(upload_to, str) else original_name
        else:
            dest = os.path.join(upload_to, original_name)
        # normalize
        dest = dest.replace('\\', '/').lstrip('/')
        # prepend uuid to avoid collisions while keeping basename readable
        base = os.path.basename(dest)
        dirname = os.path.dirname(dest)
        name = f"{uuid.uuid4().hex}-{base}"
        return f"{dirname}/{name}" if dirname else name

    def process_admin_form_files(self, request, obj, form):
        """Process uploaded files in a regular ModelAdmin form before saving the object to ensure they are uploaded to S3."""
        # iterate ImageFields on model
        for field in obj._meta.get_fields():
            if isinstance(field, models.ImageField):
                fname = field.name
                if fname in form.changed_data:
                    uploaded = form.cleaned_data.get(fname)
                    if uploaded:
                        # uploaded is InMemoryUploadedFile / TemporaryUploadedFile
                        key = self._compute_field_key(obj, field, uploaded.name)
                        ok, err = self._upload_file_to_s3(uploaded, key)
                        if ok:
                            # set the attribute to the key so saving the model writes the path
                            setattr(obj, fname, key)
                        else:
                            # if upload failed, leave form to handle fallback
                            try:
                                self.message_user(request, level=40, message=f'Failed to upload {fname} to S3: {err}')
                            except Exception:
                                pass

    def process_inline_form(self, request, inline_form):
        """Process a single inline form (for ImageBlock etc.)"""
        instance = inline_form.instance
        # find image fields
        for field in instance._meta.get_fields():
            if isinstance(field, models.ImageField):
                fname = field.name
                if fname in inline_form.changed_data:
                    uploaded = inline_form.cleaned_data.get(fname)
                    if uploaded:
                        key = self._compute_field_key(instance, field, uploaded.name)
                        ok, err = self._upload_file_to_s3(uploaded, key)
                        if ok:
                            setattr(instance, fname, key)
                        else:
                            try:
                                self.message_user(request, level=40, message=f'Failed to upload {fname} to S3: {err}')
                            except Exception:
                                pass
                            raise Exception(f'Failed to upload {fname} to S3: {err}')

    def save_model(self, request, obj, form, change):
        # process files first
        try:
            self.process_admin_form_files(request, obj, form)
        except Exception as e:
            # If processing failed, still attempt to save so admin shows error
            pass
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # process inline forms before saving
        for inline_form in formset.forms:
            if not hasattr(inline_form, 'cleaned_data'):
                continue
            try:
                self.process_inline_form(request, inline_form)
            except Exception as e:
                # propagate so admin shows error
                raise
        super().save_formset(request, form, formset, change)

class ImageBlockInline(admin.TabularInline):
    model = ImageBlock
    extra = 1

class HeroSlideAdmin(S3AdminUploadMixin, admin.ModelAdmin):
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

class HeaderAdmin(S3AdminUploadMixin, admin.ModelAdmin):
    def logo_tag(self, obj):
        if getattr(obj, 'logo', None):
            try:
                return format_html('<img src="{}" style="height:80px; object-fit:contain;" />', obj.logo.url)
            except Exception:
                return obj.logo
        return '-'
    logo_tag.short_description = 'Preview'

    list_display = ('id', 'phone', 'email', 'logo_tag')
    readonly_fields = ('logo_tag',)
    filter_horizontal = ('nav_links',)
    search_fields = ('phone', 'email')

class PageAdmin(S3AdminUploadMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageBlockInline]
    search_fields = ('title', 'slug')
    ordering = ('order',)

class AboutAdmin(S3AdminUploadMixin, admin.ModelAdmin):
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

class DirectorAdmin(S3AdminUploadMixin, admin.ModelAdmin):
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
