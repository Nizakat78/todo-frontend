#!/usr/bin/env python3
"""
Test script for JWT middleware functionality
Tests both valid and invalid token scenarios
"""

import requests
import json
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from backend.utils.jwt_handler import create_access_token, verify_token

# Base URL for the backend API
BASE_URL = "http://localhost:8000/api"

# Test user ID for creating tokens
TEST_USER_ID = "test-user-123"

def test_valid_token():
    """Test API access with a valid JWT token"""
    print("\n=== Testing Valid Token ===")

    # Create a valid token
    token = create_access_token(data={"sub": TEST_USER_ID})
    print(f"Created valid token for user: {TEST_USER_ID}")

    # Prepare headers with the valid token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Make a request to get tasks (should succeed)
    try:
        response = requests.get(f"{BASE_URL}/{TEST_USER_ID}/tasks", headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Valid token test PASSED - API accepted the valid token")
        elif response.status_code == 404:  # Expected if no tasks exist
            print("✓ Valid token test PASSED - API accepted the valid token (no tasks found)")
        else:
            print(f"✗ Valid token test FAILED - Unexpected status code: {response.status_code}")

    except Exception as e:
        print(f"✗ Valid token test ERROR: {str(e)}")

def test_invalid_token():
    """Test API access with an invalid JWT token"""
    print("\n=== Testing Invalid Token ===")

    # Create an invalid token (manually crafted or tampered)
    invalid_token = "invalid.token.here"

    # Prepare headers with the invalid token
    headers = {
        "Authorization": f"Bearer {invalid_token}",
        "Content-Type": "application/json"
    }

    # Make a request to get tasks (should fail with 401)
    try:
        response = requests.get(f"{BASE_URL}/{TEST_USER_ID}/tasks", headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 401:
            print("✓ Invalid token test PASSED - API rejected the invalid token")
        else:
            print(f"✗ Invalid token test FAILED - Expected 401, got {response.status_code}")

    except Exception as e:
        print(f"✗ Invalid token test ERROR: {str(e)}")

def test_expired_token():
    """Test API access with an expired JWT token"""
    print("\n=== Testing Expired Token ===")

    # Create an expired token (set expiry to past time)
    expired_token = create_access_token(
        data={"sub": TEST_USER_ID},
        expires_delta=timedelta(seconds=-1)  # Expired 1 second ago
    )
    print(f"Created expired token for user: {TEST_USER_ID}")

    # Prepare headers with the expired token
    headers = {
        "Authorization": f"Bearer {expired_token}",
        "Content-Type": "application/json"
    }

    # Make a request to get tasks (should fail with 401)
    try:
        response = requests.get(f"{BASE_URL}/{TEST_USER_ID}/tasks", headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 401:
            print("✓ Expired token test PASSED - API rejected the expired token")
        else:
            print(f"✗ Expired token test FAILED - Expected 401, got {response.status_code}")

    except Exception as e:
        print(f"✗ Expired token test ERROR: {str(e)}")

def test_no_token():
    """Test API access without any token"""
    print("\n=== Testing No Token ===")

    # Prepare headers without token
    headers = {
        "Content-Type": "application/json"
    }

    # Make a request to get tasks (should fail with 401)
    try:
        response = requests.get(f"{BASE_URL}/{TEST_USER_ID}/tasks", headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 401:
            print("✓ No token test PASSED - API rejected request without token")
        else:
            print(f"✗ No token test FAILED - Expected 401, got {response.status_code}")

    except Exception as e:
        print(f"✗ No token test ERROR: {str(e)}")

def test_wrong_user_id():
    """Test API access with valid token but mismatched user_id in URL"""
    print("\n=== Testing Wrong User ID in URL ===")

    # Create a valid token for test user
    token = create_access_token(data={"sub": TEST_USER_ID})
    print(f"Created valid token for user: {TEST_USER_ID}")

    # Use a different user ID in the URL than the one in the token
    different_user_id = "different-user-456"
    print(f"Using different user ID in URL: {different_user_id}")

    # Prepare headers with the valid token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Make a request to get tasks for different user (should fail with 403)
    try:
        response = requests.get(f"{BASE_URL}/{different_user_id}/tasks", headers=headers)
        print(f"Response Status: {response.status_code}")

        if response.status_code == 403:
            print("✓ Wrong user ID test PASSED - API rejected request for different user")
        else:
            print(f"✗ Wrong user ID test FAILED - Expected 403, got {response.status_code}")

    except Exception as e:
        print(f"✗ Wrong user ID test ERROR: {str(e)}")

def main():
    """Run all JWT middleware tests"""
    print("Testing JWT Middleware Functionality")
    print("=" * 50)

    # Check if backend is running
    try:
        health_check = requests.get(f"{BASE_URL}/health")
        print(f"Backend health check: {health_check.status_code}")
    except requests.exceptions.ConnectionError:
        print("⚠ WARNING: Cannot connect to backend. Make sure the FastAPI server is running on localhost:8000")
        print("Run 'uvicorn backend.main:app --reload' in another terminal to start the server")
        return

    test_valid_token()
    test_invalid_token()
    test_expired_token()
    test_no_token()
    test_wrong_user_id()

    print("\n" + "=" * 50)
    print("JWT Middleware Testing Complete")

if __name__ == "__main__":
    main()