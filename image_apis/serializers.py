from rest_framework import serializers
from .models import ProcessedImage

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = ['original_image']
    
    def validate_original_image(self, value):
        # Validate file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large. Maximum size is 10MB.")
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type. Please upload JPEG, PNG, or WebP images.")
        
        return value

class ProcessedImageSerializer(serializers.ModelSerializer):
    original_image_url = serializers.SerializerMethodField()
    processed_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessedImage
        fields = ['id', 'original_image_url', 'processed_image_url', 'processing_type', 
                 'created_at', 'processing_time']
    
    def get_original_image_url(self, obj):
        if obj.original_image:
            return self.context['request'].build_absolute_uri(obj.original_image.url)
        return None
    
    def get_processed_image_url(self, obj):
        if obj.processed_image:
            return self.context['request'].build_absolute_uri(obj.processed_image.url)
        return None 