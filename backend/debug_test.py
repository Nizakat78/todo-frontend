#!/usr/bin/env python3
"""Debug script to test the signup endpoint"""

import requests
import traceback

def test_signup():
    """Test the signup endpoint"""
    url = "http://127.0.0.1:8000/api/auth/signup"
    data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        print(f"Response Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"Request failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing signup endpoint...")
    test_signup()