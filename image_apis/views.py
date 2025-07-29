from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
import time
from .models import ProcessedImage
from .serializers import ImageUploadSerializer, ProcessedImageSerializer
from .image_processing import (
    upscale_image, remove_background, remove_object, enhance_image_quality,
    upscale_image_advanced, remove_background_advanced, remove_object_advanced, enhance_image_quality_advanced
)
from django.core.files import File

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upscale_image_api(request):
    """
    API endpoint for image upscaling
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='upscale'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image
            output_path, processing_time = upscale_image(image_path, scale_factor=2)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upscale_image_advanced_api(request):
    """
    Advanced API endpoint for image upscaling using AI models
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get scale factor from request, default to 4
            scale_factor = int(request.data.get('scale_factor', 4))
            
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='upscale_advanced'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image with advanced algorithm
            output_path, processing_time = upscale_image_advanced(image_path, scale_factor=scale_factor)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def remove_background_api(request):
    """
    API endpoint for background removal
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='background_removal'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image
            output_path, processing_time = remove_background(image_path)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def remove_background_advanced_api(request):
    """
    Advanced API endpoint for background removal using multiple AI models
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='background_removal_advanced'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image with advanced algorithm
            output_path, processing_time = remove_background_advanced(image_path)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def remove_object_api(request):
    """
    API endpoint for object removal
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get coordinates from request
            x1 = int(request.data.get('x1', 0))
            y1 = int(request.data.get('y1', 0))
            x2 = int(request.data.get('x2', 0))
            y2 = int(request.data.get('y2', 0))
            
            if x1 >= x2 or y1 >= y2:
                return Response(
                    {'error': 'Invalid coordinates. x2 must be greater than x1 and y2 must be greater than y1.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='object_removal'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image
            output_path, processing_time = remove_object(image_path, x1, y1, x2, y2)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def remove_object_advanced_api(request):
    """
    Advanced API endpoint for object removal using multiple inpainting methods
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get coordinates from request
            x1 = int(request.data.get('x1', 0))
            y1 = int(request.data.get('y1', 0))
            x2 = int(request.data.get('x2', 0))
            y2 = int(request.data.get('y2', 0))
            
            if x1 >= x2 or y1 >= y2:
                return Response(
                    {'error': 'Invalid coordinates. x2 must be greater than x1 and y2 must be greater than y1.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='object_removal_advanced'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image with advanced algorithm
            output_path, processing_time = remove_object_advanced(image_path, x1, y1, x2, y2)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def enhance_image_api(request):
    """
    API endpoint for image enhancement
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='enhancement'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image
            output_path, processing_time = enhance_image_quality(image_path)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def enhance_image_advanced_api(request):
    """
    Advanced API endpoint for image enhancement using AI models
    """
    try:
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create ProcessedImage instance
            processed_image = ProcessedImage.objects.create(
                original_image=serializer.validated_data['original_image'],
                processing_type='enhancement_advanced'
            )
            
            # Get the file path
            image_path = processed_image.original_image.path
            
            # Process the image with advanced algorithm
            output_path, processing_time = enhance_image_quality_advanced(image_path)
            
            # Save the processed image
            with open(output_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(output_path),
                    File(f),
                    save=True
                )
            
            # Update processing time
            processed_image.processing_time = processing_time
            processed_image.save()
            
            # Clean up temporary file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return response
            response_serializer = ProcessedImageSerializer(
                processed_image, 
                context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_processed_images(request):
    """
    API endpoint to get all processed images
    """
    try:
        processed_images = ProcessedImage.objects.all()
        serializer = ProcessedImageSerializer(
            processed_images, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_processed_image(request, image_id):
    """
    API endpoint to get a specific processed image
    """
    try:
        processed_image = ProcessedImage.objects.get(id=image_id)
        serializer = ProcessedImageSerializer(
            processed_image, 
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except ProcessedImage.DoesNotExist:
        return Response(
            {'error': 'Image not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
