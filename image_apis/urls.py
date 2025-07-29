from django.urls import path
from . import views

urlpatterns = [
    # Basic Image processing APIs
    path('upscale/', views.upscale_image_api, name='upscale_image'),
    path('remove-background/', views.remove_background_api, name='remove_background'),
    path('remove-object/', views.remove_object_api, name='remove_object'),
    path('enhance/', views.enhance_image_api, name='enhance_image'),
    
    # Advanced Image processing APIs (AI-powered)
    path('upscale-advanced/', views.upscale_image_advanced_api, name='upscale_image_advanced'),
    path('remove-background-advanced/', views.remove_background_advanced_api, name='remove_background_advanced'),
    path('remove-object-advanced/', views.remove_object_advanced_api, name='remove_object_advanced'),
    path('enhance-advanced/', views.enhance_image_advanced_api, name='enhance_image_advanced'),
    
    # Get processed images
    path('processed-images/', views.get_processed_images, name='get_processed_images'),
    path('processed-images/<int:image_id>/', views.get_processed_image, name='get_processed_image'),
] 