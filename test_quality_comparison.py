#!/usr/bin/env python3
"""
Quality Comparison Test Script
Compares basic vs advanced image processing methods
"""

import requests
import time
import os
from PIL import Image
import io

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_image_processing(image_path, test_name):
    """Test both basic and advanced processing for comparison"""
    
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"Image: {image_path}")
    print(f"{'='*60}")
    
    # Test basic processing
    print("\n🔧 Testing BASIC processing...")
    basic_start = time.time()
    
    try:
        with open(image_path, 'rb') as f:
            files = {'original_image': f}
            response = requests.post(f"{BASE_URL}/remove-background/", files=files)
            
        if response.status_code == 201:
            basic_time = time.time() - basic_start
            basic_data = response.json()
            print(f"✅ Basic processing completed in {basic_time:.2f}s")
            print(f"   Processing time: {basic_data.get('processing_time', 'N/A')}s")
            print(f"   Result URL: {basic_data.get('processed_image', 'N/A')}")
        else:
            print(f"❌ Basic processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Basic processing error: {e}")
    
    # Test advanced processing
    print("\n🚀 Testing ADVANCED processing...")
    advanced_start = time.time()
    
    try:
        with open(image_path, 'rb') as f:
            files = {'original_image': f}
            response = requests.post(f"{BASE_URL}/remove-background-advanced/", files=files)
            
        if response.status_code == 201:
            advanced_time = time.time() - advanced_start
            advanced_data = response.json()
            print(f"✅ Advanced processing completed in {advanced_time:.2f}s")
            print(f"   Processing time: {advanced_data.get('processing_time', 'N/A')}s")
            print(f"   Result URL: {advanced_data.get('processed_image', 'N/A')}")
        else:
            print(f"❌ Advanced processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Advanced processing error: {e}")
    
    # Test upscaling comparison
    print("\n📈 Testing upscaling comparison...")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'original_image': f}
            response = requests.post(f"{BASE_URL}/upscale-advanced/", files=files)
            
        if response.status_code == 201:
            upscale_data = response.json()
            print(f"✅ Advanced upscaling completed")
            print(f"   Result URL: {upscale_data.get('processed_image', 'N/A')}")
        else:
            print(f"❌ Advanced upscaling failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Advanced upscaling error: {e}")

def test_enhancement(image_path):
    """Test image enhancement"""
    print(f"\n🎨 Testing image enhancement...")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'original_image': f}
            response = requests.post(f"{BASE_URL}/enhance-advanced/", files=files)
            
        if response.status_code == 201:
            enhance_data = response.json()
            print(f"✅ Advanced enhancement completed")
            print(f"   Result URL: {enhance_data.get('processed_image', 'N/A')}")
        else:
            print(f"❌ Advanced enhancement failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Advanced enhancement error: {e}")

def main():
    """Main test function"""
    print("🧪 Image Processing Quality Comparison Test")
    print("=" * 60)
    
    # Test with available images
    test_images = [
        "test_upscale.jpg",
        # Add more test images here
    ]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            test_image_processing(image_path, "Background Removal")
            test_enhancement(image_path)
        else:
            print(f"⚠️  Test image not found: {image_path}")
    
    print(f"\n{'='*60}")
    print("🎯 Quality Comparison Summary")
    print("=" * 60)
    print("""
    Expected Quality Improvements:
    
    🔹 Background Removal:
       - Better edge accuracy (especially hair/fur)
       - Reduced artifacts and noise
       - Smoother alpha channel
    
    🔹 Upscaling:
       - 4x resolution with AI-generated details
       - Face-specific enhancement
       - Better texture preservation
    
    🔹 Enhancement:
       - Better color accuracy
       - Enhanced details and sharpness
       - Reduced noise while preserving details
    
    ⚠️  Note: Advanced processing takes longer but produces much better results!
    """)

if __name__ == "__main__":
    main() 