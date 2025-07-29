import cv2
import numpy as np
from PIL import Image
import io
import time
import os
from rembg import remove, new_session

def upscale_image_advanced(image_path, scale_factor=4):
    """
    Advanced upscaling using enhanced basic methods
    """
    start_time = time.time()
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    
    # Enhanced basic upscaling
    upscaled = enhanced_basic_upscaling(img, scale_factor)
    
    # Apply final enhancement
    upscaled = enhance_final_quality(upscaled)
    
    # Save the upscaled image
    output_path = image_path.replace('.', '_upscaled_advanced.')
    cv2.imwrite(output_path, upscaled)
    
    processing_time = time.time() - start_time
    return output_path, processing_time

def enhanced_basic_upscaling(img, scale_factor):
    """Enhanced basic upscaling with better algorithms"""
    # Get original dimensions
    height, width = img.shape[:2]
    
    # Calculate new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Use Lanczos interpolation for better quality
    upscaled = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Apply advanced sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(upscaled, -1, kernel)
    
    # Blend original and sharpened
    upscaled = cv2.addWeighted(upscaled, 0.7, sharpened, 0.3, 0)
    
    return upscaled

def remove_background_advanced(image_path):
    """
    Advanced background removal using enhanced rembg
    """
    start_time = time.time()
    
    # Read image
    input_image = Image.open(image_path)
    
    # Use rembg with improved session
    session = new_session("u2net")
    output_image = remove(input_image, session=session)
    
    # Apply post-processing for better quality
    output_image = post_process_background_removal(output_image)
    
    # Save the processed image
    output_path = image_path.replace('.', '_no_bg_advanced.')
    output_image.save(output_path, 'PNG', optimize=True)
    
    processing_time = time.time() - start_time
    return output_path, processing_time

def remove_object_advanced(image_path, x1, y1, x2, y2):
    """
    Advanced object removal using multiple inpainting methods
    """
    start_time = time.time()
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    
    # Create mask for the region to remove
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255
    
    # Method 1: OpenCV Telea inpainting
    result_telea = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # Method 2: OpenCV NS inpainting
    result_ns = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    
    # Method 3: Advanced inpainting with edge-aware blending
    result_advanced = advanced_inpainting(img, mask)
    
    # Blend results for better quality
    result = blend_inpainting_results(result_telea, result_ns, result_advanced, mask)
    
    # Apply post-processing
    result = post_process_inpainting(result, mask)
    
    # Save the processed image
    output_path = image_path.replace('.', '_object_removed_advanced.')
    cv2.imwrite(output_path, result)
    
    processing_time = time.time() - start_time
    return output_path, processing_time

def enhance_image_quality_advanced(image_path):
    """
    Advanced image enhancement using multiple techniques
    """
    start_time = time.time()
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    
    # Step 1: Noise reduction
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # Step 2: Super resolution for small images
    height, width = img.shape[:2]
    if height < 512 or width < 512:
        img = enhanced_basic_upscaling(img, 2)
    
    # Step 3: Color enhancement
    img = enhance_colors(img)
    
    # Step 4: Sharpening
    img = adaptive_sharpening(img)
    
    # Step 5: Contrast enhancement
    img = enhance_contrast(img)
    
    # Step 6: Final quality boost
    img = enhance_final_quality(img)
    
    # Save the enhanced image
    output_path = image_path.replace('.', '_enhanced_advanced.')
    cv2.imwrite(output_path, img)
    
    processing_time = time.time() - start_time
    return output_path, processing_time

# Helper functions for advanced processing

def enhance_final_quality(img):
    """Apply final quality enhancements"""
    # Convert to LAB for better processing
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Apply slight Gaussian blur to reduce artifacts
    enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0.5)
    
    return enhanced

def post_process_background_removal(image):
    """Post-process background removal result"""
    # Convert to numpy array
    img_array = np.array(image)
    
    if img_array.shape[2] == 4:  # RGBA
        # Apply edge smoothing
        alpha = img_array[:, :, 3]
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
        img_array[:, :, 3] = alpha
        
        # Remove artifacts
        kernel = np.ones((2, 2), np.uint8)
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)
        img_array[:, :, 3] = alpha
    
    return Image.fromarray(img_array)

def advanced_inpainting(img, mask):
    """Advanced inpainting with multiple passes"""
    # Create a larger mask for better context
    kernel = np.ones((5, 5), np.uint8)
    expanded_mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Multi-scale inpainting
    result = img.copy()
    
    # First pass: large scale
    result = cv2.inpaint(result, expanded_mask, 5, cv2.INPAINT_TELEA)
    
    # Second pass: original scale
    result = cv2.inpaint(result, mask, 3, cv2.INPAINT_NS)
    
    return result

def blend_inpainting_results(result1, result2, result3, mask):
    """Blend multiple inpainting results"""
    # Create weight mask based on distance from mask edge
    distance = cv2.distanceTransform(255 - mask, cv2.DIST_L2, 5)
    distance = np.clip(distance / distance.max(), 0, 1)
    
    # Blend results
    blended = (result1 * distance[:, :, np.newaxis] + 
               result2 * (1 - distance[:, :, np.newaxis]) * 0.5 +
               result3 * (1 - distance[:, :, np.newaxis]) * 0.5)
    
    return blended.astype(np.uint8)

def post_process_inpainting(result, mask):
    """Post-process inpainting result"""
    # Apply slight blur to mask edges
    kernel = np.ones((3, 3), np.uint8)
    blurred_mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Blend original and inpainted result
    alpha = blurred_mask / 255.0
    result = result * alpha[:, :, np.newaxis] + result * (1 - alpha[:, :, np.newaxis])
    
    return result.astype(np.uint8)

def enhance_colors(img):
    """Enhance colors using multiple techniques"""
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Enhance saturation
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)
    
    # Enhance value
    hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.1)
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return enhanced

def adaptive_sharpening(img):
    """Apply adaptive sharpening"""
    # Create sharpening kernel
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    
    # Apply sharpening
    sharpened = cv2.filter2D(img, -1, kernel)
    
    # Blend with original
    result = cv2.addWeighted(img, 0.7, sharpened, 0.3, 0)
    
    return result

def enhance_contrast(img):
    """Enhance contrast using CLAHE"""
    # Convert to LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    return enhanced

# Keep original functions for backward compatibility
def upscale_image(image_path, scale_factor=2):
    """Original upscaling function - now calls advanced version"""
    return upscale_image_advanced(image_path, scale_factor)

def remove_background(image_path):
    """Original background removal function - now calls advanced version"""
    return remove_background_advanced(image_path)

def remove_object(image_path, x1, y1, x2, y2):
    """Original object removal function - now calls advanced version"""
    return remove_object_advanced(image_path, x1, y1, x2, y2)

def enhance_image_quality(image_path):
    """Original enhancement function - now calls advanced version"""
    return enhance_image_quality_advanced(image_path) 