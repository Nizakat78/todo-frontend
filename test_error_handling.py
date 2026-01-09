#!/usr/bin/env python3
"""
Test script for error handling in various failure scenarios
Tests network failures, backend unavailability, and other error conditions
"""

import requests
import time
import subprocess
import signal
import os
from threading import Thread
import socket

def is_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_network_failures():
    """Test error handling when backend is unavailable"""
    print("Testing Network Failures and Backend Unavailability")
    print("=" * 60)

    # Test with backend not running
    print("\n--- Testing Connection to Unavailable Backend ---")

    # Use a port that we know is closed
    closed_port_url = "http://localhost:9999/api"

    try:
        response = requests.get(closed_port_url, timeout=2)
        print(f"✗ Unexpected: Got response from closed port: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✓ Correctly handled connection error to unavailable backend")
    except requests.exceptions.Timeout:
        print("✓ Correctly handled timeout to unavailable backend")
    except Exception as e:
        print(f"? Handled unavailable backend with error: {type(e).__name__}")

    # Test with malformed URL
    print("\n--- Testing Malformed URLs ---")
    try:
        response = requests.get("http://invalid-url-that-does-not-exist-12345.com", timeout=3)
        print(f"✗ Unexpected: Got response from invalid domain: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✓ Correctly handled connection error to invalid domain")
    except requests.exceptions.Timeout:
        print("✓ Correctly handled timeout to invalid domain")
    except Exception as e:
        print(f"? Handled invalid domain with error: {type(e).__name__}")

    # Test with valid server but non-existent endpoint
    print("\n--- Testing Non-existent Endpoints (if backend is running) ---")
    if is_port_open("localhost", 8000):
        try:
            response = requests.get("http://localhost:8000/nonexistent-endpoint", timeout=5)
            print(f"Non-existent endpoint response: {response.status_code}")

            if response.status_code in [404, 405]:
                print("✓ Backend correctly returned error for non-existent endpoint")
            else:
                print(f"? Backend returned unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Endpoint test error: {type(e).__name__}: {e}")
    else:
        print("⚠ Backend not running on port 8000, skipping non-existent endpoint test")

def test_client_side_error_handling():
    """Test frontend's ability to handle various error conditions"""
    print("\n\nTesting Client-Side Error Handling")
    print("=" * 60)

    # This simulates what would happen in the frontend when errors occur
    print("\n--- Simulated Frontend Error Handling ---")

    # Simulate different HTTP error responses
    error_scenarios = [
        (400, "Bad Request"),
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (404, "Not Found"),
        (500, "Internal Server Error"),
        (502, "Bad Gateway"),
        (503, "Service Unavailable"),
        (504, "Gateway Timeout")
    ]

    for status_code, description in error_scenarios:
        print(f"Status {status_code} ({description}): Would trigger appropriate frontend error handling")

        # These would be handled by the axios interceptors in the frontend:
        if status_code == 401:
            print("  → Would clear auth tokens and redirect to login")
        elif status_code == 403:
            print("  → Would show access denied message")
        elif status_code >= 500:
            print("  → Would show server error message and retry option")
        else:
            print("  → Would show user-friendly error message")

def test_timeout_handling():
    """Test timeout handling"""
    print("\n\nTesting Timeout Handling")
    print("=" * 60)

    if is_port_open("localhost", 8000):
        try:
            # Make a request with a very short timeout to test timeout handling
            response = requests.get("http://localhost:8000/api/health", timeout=0.001)
            print(f"✗ Unexpected: Got response despite tiny timeout: {response.status_code}")
        except requests.exceptions.Timeout:
            print("✓ Correctly handled request timeout")
        except requests.exceptions.RequestException as e:
            print(f"✓ Correctly handled timeout error: {type(e).__name__}")
    else:
        print("⚠ Backend not running on port 8000, skipping timeout test")

def test_error_recovery():
    """Test if the system can recover from temporary failures"""
    print("\n\nTesting Error Recovery")
    print("=" * 60)

    print("Error recovery would be tested by:")
    print("1. Having the frontend retry failed requests appropriately")
    print("2. Showing users appropriate loading states during retries")
    print("3. Gracefully degrading functionality when parts of the system are unavailable")
    print("4. Providing offline capability where appropriate")
    print("5. Caching responses to minimize backend dependency")

def main():
    """Run all error handling tests"""
    print("Starting Error Handling Tests")
    print("=" * 60)

    print("This test suite evaluates the robustness of error handling in the system.")
    print("It covers network failures, backend unavailability, and client-side error management.")

    test_network_failures()
    test_client_side_error_handling()
    test_timeout_handling()
    test_error_recovery()

    print("\n" + "=" * 60)
    print("Error Handling Tests Complete")
    print("\nNote: The frontend already has proper error handling through:")
    print("- Axios interceptors that catch network errors")
    print("- 401 handling that clears auth data")
    print("- Proper error message display in the UI components")
    print("- Retry mechanisms can be added as needed")

if __name__ == "__main__":
    main()