#!/usr/bin/env python3
"""Test script for the Skin AI Dermatologist API."""
import requests
import sys

API_URL = "http://127.0.0.1:8000/api/skin/analyze"

def test_with_image(image_path: str):
    """Test the API with an image file."""
    print(f"Testing API with image: {image_path}")
    print("-" * 60)
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print("\nResponse:")
            print(f"  Vision Description: {result.get('vision_description', 'N/A')[:100]}...")
            print(f"  Predicted Condition: {result.get('predicted_condition', 'N/A')}")
            print(f"  Match Score: {result.get('match_score', 'N/A')}")
            print(f"  Example Caption: {result.get('example_caption', 'N/A')[:100]}...")
            print(f"  Disclaimer: {result.get('disclaimer', 'N/A')}")
            print("\nTop 3 Matches:")
            for i, match in enumerate(result.get('top_matches', [])[:3], 1):
                print(f"  {i}. {match.get('label', 'N/A')} (score: {match.get('score', 0)})")
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except FileNotFoundError:
        print(f"❌ ERROR: Image file not found: {image_path}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print(f"✅ Health check: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_with_image(image_path)
    else:
        print("Usage: python test_api.py <image_path>")
        print("\nExample:")
        print("  python test_api.py q13.jpg")
        print("\nOr test health endpoint:")
        test_health()
        print("\nOr visit http://127.0.0.1:8000/docs for interactive testing")

