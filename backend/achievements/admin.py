from django.contrib import admin
from .models import Certificate

# import S3AdminUploadMixin from content admin to reuse upload behavior
try:
    from content.admin import S3AdminUploadMixin
except Exception:
    S3AdminUploadMixin = object

@admin.register(Certificate)
class CertificateAdmin(S3AdminUploadMixin, admin.ModelAdmin):
    list_display = ['title', 'year', 'category', 'level', 'order', 'created_at']
    list_filter = ['category', 'level', 'year']
    search_fields = ['title', 'year']
    list_editable = ['order']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('Негізгі ақпарат', {
            'fields': ('title', 'year', 'image')
        }),
        ('Жіктеу', {
            'fields': ('category', 'level', 'order')
        }),
    )