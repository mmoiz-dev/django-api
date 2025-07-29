from django.db import models
import os
import uuid

def get_upload_path(instance, filename):
    """Generate unique upload path for images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('processed_images', filename)

class ProcessedImage(models.Model):
    PROCESSING_TYPES = [
        ('upscale', 'Image Upscaler'),
        ('background_removal', 'Background Remover'),
        ('object_removal', 'Object Remover'),
    ]
    
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    processing_type = models.CharField(max_length=20, choices=PROCESSING_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_processing_type_display()} - {self.created_at}"
