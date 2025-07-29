from django.contrib import admin
from .models import ProcessedImage

@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'processing_type', 'created_at', 'processing_time']
    list_filter = ['processing_type', 'created_at']
    search_fields = ['processing_type']
    readonly_fields = ['created_at', 'processing_time']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('original_image', 'processed_image', 'processing_type')
        }),
        ('Processing Details', {
            'fields': ('created_at', 'processing_time'),
            'classes': ('collapse',)
        }),
    )
