from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
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