"""
Test script for Shelf-Eye Agent API
"""

import requests
import json
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8080"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_standards():
    """Test getting reference standards"""
    print("📋 Testing reference standards endpoint...")
    response = requests.get(f"{API_URL}/standards")
    print(f"Status: {response.status_code}")
    print(f"Standards: {json.dumps(response.json(), indent=2)}")
    print()

def test_audit_shelf(image_path):
    """Test shelf audit with an image"""
    print(f"🔍 Testing shelf audit with image: {image_path}")
    
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found at {image_path}")
        return
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_URL}/audit", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success!")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Section: {result['reference_section']}")
        print(f"\n📊 Analysis Results:\n")
        print(result['analysis'])
    else:
        print(f"❌ Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("🛒 Shelf-Eye Agent - API Test Suite")
    print("=" * 60)
    print()
    
    # Test health check
    test_health_check()
    
    # Test standards endpoint
    test_get_standards()
    
    # Test shelf audit (you need to provide an image path)
    # Uncomment and update the path below to test with an actual image
    # test_audit_shelf("path/to/your/shelf-image.jpg")
    
    print("=" * 60)
    print("✅ Test suite completed!")
    print("=" * 60)
