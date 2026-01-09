#!/usr/bin/env python3
"""
Test script to verify 401 responses for invalid tokens
"""

import requests
import json
from backend.utils.jwt_handler import create_access_token

# Base URL for the backend API
BASE_URL = "http://localhost:8000/api"

def test_401_responses():
    """Test that all endpoints return proper 401 responses for invalid tokens"""
    print("Testing 401 Responses for Invalid Tokens")
    print("=" * 50)

    # Test user ID
    test_user_id = "test-user-123"

    # Test with invalid token
    invalid_token = "invalid.token.string"

    # Test with expired token
    expired_token = create_access_token(
        data={"sub": test_user_id},
        expires_delta=-1  # Negative value to make it expired
    )

    headers_invalid = {
        "Authorization": f"Bearer {invalid_token}",
        "Content-Type": "application/json"
    }

    headers_expired = {
        "Authorization": f"Bearer {expired_token}",
        "Content-Type": "application/json"
    }

    # Define test endpoints
    endpoints = [
        ("GET", f"/{test_user_id}/tasks"),
        ("GET", f"/{test_user_id}/tasks/1"),
        ("POST", f"/{test_user_id}/tasks"),
        ("PUT", f"/{test_user_id}/tasks/1"),
        ("PATCH", f"/{test_user_id}/tasks/1/complete"),
        ("DELETE", f"/{test_user_id}/tasks/1"),
    ]

    print("Testing with INVALID token:")
    print("-" * 30)
    for method, endpoint in endpoints:
        try:
            url = BASE_URL + endpoint
            if method == "GET":
                response = requests.get(url, headers=headers_invalid)
            elif method == "POST":
                response = requests.post(url, headers=headers_invalid, json={"title": "Test"})
            elif method == "PUT":
                response = requests.put(url, headers=headers_invalid, json={"title": "Updated"})
            elif method == "PATCH":
                response = requests.patch(url, headers=headers_invalid, json={"completed": True})
            elif method == "DELETE":
                response = requests.delete(url, headers=headers_invalid)

            expected_status = 401
            status_ok = response.status_code == expected_status
            print(f"{method} {endpoint:<30} -> {response.status_code} {'✓' if status_ok else '✗'}")

            if not status_ok:
                print(f"  Expected: {expected_status}, Got: {response.status_code}")

        except Exception as e:
            print(f"{method} {endpoint:<30} -> ERROR: {str(e)}")

    print("\nTesting with EXPIRED token:")
    print("-" * 30)
    for method, endpoint in endpoints:
        try:
            url = BASE_URL + endpoint
            if method == "GET":
                response = requests.get(url, headers=headers_expired)
            elif method == "POST":
                response = requests.post(url, headers=headers_expired, json={"title": "Test"})
            elif method == "PUT":
                response = requests.put(url, headers=headers_expired, json={"title": "Updated"})
            elif method == "PATCH":
                response = requests.patch(url, headers=headers_expired, json={"completed": True})
            elif method == "DELETE":
                response = requests.delete(url, headers=headers_expired)

            expected_status = 401
            status_ok = response.status_code == expected_status
            print(f"{method} {endpoint:<30} -> {response.status_code} {'✓' if status_ok else '✗'}")

            if not status_ok:
                print(f"  Expected: {expected_status}, Got: {response.status_code}")

        except Exception as e:
            print(f"{method} {endpoint:<30} -> ERROR: {str(e)}")

    # Test with no token at all
    print("\nTesting with NO token:")
    print("-" * 30)
    headers_none = {"Content-Type": "application/json"}
    for method, endpoint in endpoints:
        try:
            url = BASE_URL + endpoint
            if method == "GET":
                response = requests.get(url, headers=headers_none)
            elif method == "POST":
                response = requests.post(url, headers=headers_none, json={"title": "Test"})
            elif method == "PUT":
                response = requests.put(url, headers=headers_none, json={"title": "Updated"})
            elif method == "PATCH":
                response = requests.patch(url, headers=headers_none, json={"completed": True})
            elif method == "DELETE":
                response = requests.delete(url, headers=headers_none)

            expected_status = 401
            status_ok = response.status_code == expected_status
            print(f"{method} {endpoint:<30} -> {response.status_code} {'✓' if status_ok else '✗'}")

            if not status_ok:
                print(f"  Expected: {expected_status}, Got: {response.status_code}")

        except Exception as e:
            print(f"{method} {endpoint:<30} -> ERROR: {str(e)}")

    print("\n" + "=" * 50)
    print("401 Response Testing Complete")

if __name__ == "__main__":
    try:
        # Check if backend is running
        health_check = requests.get(f"{BASE_URL}/health")
        print(f"Backend health check: {health_check.status_code}")
        test_401_responses()
    except requests.exceptions.ConnectionError:
        print("⚠ WARNING: Cannot connect to backend. Make sure the FastAPI server is running on localhost:8000")
        print("Run 'uvicorn backend.main:app --reload' in another terminal to start the server")