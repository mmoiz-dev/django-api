#!/usr/bin/env python3
"""
Test script for the Django Image Processing API
"""

import requests
import json
import os
from PIL import Image
import numpy as np

# API base URL
BASE_URL = "http://localhost:8000/api"

def create_test_image(filename="test_image.jpg", size=(300, 300)):
    """Create a test image for testing"""
    # Create a simple test image with some shapes
    img = Image.new('RGB', size, color='white')
    
    # Draw some shapes
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Draw a red circle
    draw.ellipse([50, 50, 150, 150], fill='red')
    
    # Draw a blue rectangle
    draw.rectangle([200, 100, 280, 200], fill='blue')
    
    # Draw a green triangle
    draw.polygon([(100, 250), (150, 200), (200, 250)], fill='green')
    
    img.save(filename)
    return filename

def test_upscale_api():
    """Test the image upscaling API"""
    print("Testing Image Upscaler API...")
    
    # Create test image
    test_image = create_test_image("test_upscale.jpg")
    
    # Prepare the request
    url = f"{BASE_URL}/upscale/"
    files = {'original_image': open(test_image, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Upscale API Test Passed!")
            print(f"Processing Time: {data.get('processing_time', 'N/A')} seconds")
            print(f"Original Image URL: {data.get('original_image_url', 'N/A')}")
            print(f"Processed Image URL: {data.get('processed_image_url', 'N/A')}")
        else:
            print("❌ Upscale API Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing upscale API: {e}")
    
    finally:
        # Clean up test file
        if os.path.exists(test_image):
            os.remove(test_image)

def test_background_removal_api():
    """Test the background removal API"""
    print("\nTesting Background Removal API...")
    
    # Create test image
    test_image = create_test_image("test_bg_removal.jpg")
    
    # Prepare the request
    url = f"{BASE_URL}/remove-background/"
    files = {'original_image': open(test_image, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Background Removal API Test Passed!")
            print(f"Processing Time: {data.get('processing_time', 'N/A')} seconds")
            print(f"Original Image URL: {data.get('original_image_url', 'N/A')}")
            print(f"Processed Image URL: {data.get('processed_image_url', 'N/A')}")
        else:
            print("❌ Background Removal API Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing background removal API: {e}")
    
    finally:
        # Clean up test file
        if os.path.exists(test_image):
            os.remove(test_image)

def test_object_removal_api():
    """Test the object removal API"""
    print("\nTesting Object Removal API...")
    
    # Create test image
    test_image = create_test_image("test_object_removal.jpg")
    
    # Prepare the request
    url = f"{BASE_URL}/remove-object/"
    files = {'original_image': open(test_image, 'rb')}
    data = {
        'x1': 50,
        'y1': 50,
        'x2': 150,
        'y2': 150
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Object Removal API Test Passed!")
            print(f"Processing Time: {data.get('processing_time', 'N/A')} seconds")
            print(f"Original Image URL: {data.get('original_image_url', 'N/A')}")
            print(f"Processed Image URL: {data.get('processed_image_url', 'N/A')}")
        else:
            print("❌ Object Removal API Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing object removal API: {e}")
    
    finally:
        # Clean up test file
        if os.path.exists(test_image):
            os.remove(test_image)

def test_get_processed_images():
    """Test getting all processed images"""
    print("\nTesting Get Processed Images API...")
    
    url = f"{BASE_URL}/processed-images/"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get Processed Images API Test Passed!")
            print(f"Number of processed images: {len(data)}")
            for img in data:
                print(f"- ID: {img.get('id')}, Type: {img.get('processing_type')}")
        else:
            print("❌ Get Processed Images API Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing get processed images API: {e}")

def test_with_real_image(image_path):
    """Test APIs with a real image file"""
    print(f"\nTesting APIs with real image: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    # Test upscale with real image
    print("\n--- Testing Upscale with Real Image ---")
    url = f"{BASE_URL}/upscale/"
    files = {'original_image': open(image_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Real Image Upscale Test Passed!")
            print(f"Processing Time: {data.get('processing_time', 'N/A')} seconds")
            print(f"Processed Image URL: {data.get('processed_image_url', 'N/A')}")
        else:
            print("❌ Real Image Upscale Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing real image upscale: {e}")
    
    # Test background removal with real image
    print("\n--- Testing Background Removal with Real Image ---")
    url = f"{BASE_URL}/remove-background/"
    files = {'original_image': open(image_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Real Image Background Removal Test Passed!")
            print(f"Processing Time: {data.get('processing_time', 'N/A')} seconds")
            print(f"Processed Image URL: {data.get('processed_image_url', 'N/A')}")
        else:
            print("❌ Real Image Background Removal Test Failed!")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing real image background removal: {e}")

def main():
    """Run all API tests"""
    print("🚀 Starting Django Image Processing API Tests")
    print("=" * 50)
    
    # Test all APIs with generated images
    test_upscale_api()
    test_background_removal_api()
    test_object_removal_api()
    test_get_processed_images()
    
    # Test with real image if provided
    import sys
    if len(sys.argv) > 1:
        real_image_path = sys.argv[1]
        test_with_real_image(real_image_path)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📝 API Documentation:")
    print(f"- Upscale API: POST {BASE_URL}/upscale/")
    print(f"- Background Removal: POST {BASE_URL}/remove-background/")
    print(f"- Object Removal: POST {BASE_URL}/remove-object/")
    print(f"- Get All Images: GET {BASE_URL}/processed-images/")
    print(f"- Admin Interface: http://localhost:8000/admin/")
    print("\n💡 To test with a real image:")
    print("python test_api.py path/to/your/image.jpg")

if __name__ == "__main__":
    main() 