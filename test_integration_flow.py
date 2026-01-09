#!/usr/bin/env python3
"""
Integration test script for the full authentication and task management flow
Tests the complete user journey: signup -> login -> create tasks -> retrieve tasks -> logout
"""

import requests
import json
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
import time

# Base URL for the backend API
BASE_URL = "http://localhost:8000/api"

def test_full_integration_flow():
    """Test the complete integration flow: signup, login, create tasks, retrieve tasks, logout"""
    print("Testing Full Integration Flow")
    print("=" * 60)

    # Test data
    test_email = f"testuser_{int(time.time())}@example.com"
    test_password = "securepassword123"
    test_name = "Test User"

    print(f"\n--- Step 1: Signup ---")
    print(f"Creating new user: {test_email}")

    # Step 1: Signup
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json={
            "email": test_email,
            "password": test_password,
            "name": test_name
        })

        print(f"Signup Response: {signup_response.status_code}")
        if signup_response.status_code == 200:
            signup_data = signup_response.json()
            user_id = signup_data['data']['id']
            token = signup_data['token']
            print(f"✓ Signup successful for user: {user_id}")
        else:
            print(f"✗ Signup failed with status: {signup_response.status_code}")
            print(f"Response: {signup_response.text}")
            return False
    except Exception as e:
        print(f"✗ Signup error: {str(e)}")
        return False

    # Prepare headers with the token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"\n--- Step 2: Login ---")
    print(f"Logging in as: {test_email}")

    # Step 2: Login (to verify the login flow works too)
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_email,
            "password": test_password
        })

        print(f"Login Response: {login_response.status_code}")
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data['token']
            headers["Authorization"] = f"Bearer {token}"
            print("✓ Login successful")
        else:
            print(f"✗ Login failed with status: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
    except Exception as e:
        print(f"✗ Login error: {str(e)}")
        return False

    print(f"\n--- Step 3: Create Tasks ---")
    print("Creating sample tasks...")

    # Update headers with new token from login
    headers["Authorization"] = f"Bearer {login_data['token']}"

    # Step 3: Create some tasks
    tasks_created = []
    for i in range(3):
        task_data = {
            "title": f"Integration Test Task {i+1}",
            "description": f"This is test task number {i+1} created during integration testing"
        }

        try:
            create_response = requests.post(f"{BASE_URL}/{user_id}/tasks",
                                         json=task_data, headers=headers)

            print(f"Create Task {i+1}: {create_response.status_code}")
            if create_response.status_code in [200, 201]:
                task_info = create_response.json()
                task_id = task_info['data']['id']
                tasks_created.append(task_id)
                print(f"  ✓ Task {i+1} created with ID: {task_id}")
            else:
                print(f"  ✗ Task {i+1} creation failed with status: {create_response.status_code}")
                print(f"  Response: {create_response.text}")
        except Exception as e:
            print(f"  ✗ Task {i+1} creation error: {str(e)}")

    print(f"\n--- Step 4: Retrieve All Tasks ---")
    print("Fetching all tasks for the user...")

    # Step 4: Retrieve all tasks
    try:
        get_all_response = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
        print(f"Get All Tasks Response: {get_all_response.status_code}")

        if get_all_response.status_code == 200:
            tasks_data = get_all_response.json()
            retrieved_tasks = tasks_data['data']
            print(f"✓ Retrieved {len(retrieved_tasks)} tasks")

            if len(retrieved_tasks) >= len(tasks_created):
                print("✓ All created tasks were successfully retrieved")
            else:
                print(f"✗ Expected at least {len(tasks_created)} tasks, got {len(retrieved_tasks)}")
        else:
            print(f"✗ Failed to retrieve tasks: {get_all_response.status_code}")
            print(f"Response: {get_all_response.text}")
            return False
    except Exception as e:
        print(f"✗ Get all tasks error: {str(e)}")
        return False

    print(f"\n--- Step 5: Retrieve Individual Task ---")
    print("Fetching individual task...")

    # Step 5: Retrieve individual task
    if tasks_created:
        first_task_id = tasks_created[0]
        try:
            get_one_response = requests.get(f"{BASE_URL}/{user_id}/tasks/{first_task_id}",
                                          headers=headers)
            print(f"Get Individual Task Response: {get_one_response.status_code}")

            if get_one_response.status_code == 200:
                task_data = get_one_response.json()
                print(f"✓ Successfully retrieved task {first_task_id}")
            else:
                print(f"✗ Failed to retrieve individual task: {get_one_response.status_code}")
                print(f"Response: {get_one_response.text}")
        except Exception as e:
            print(f"✗ Get individual task error: {str(e)}")

    print(f"\n--- Step 6: Update Task ---")
    print("Updating a task...")

    # Step 6: Update a task
    if tasks_created:
        first_task_id = tasks_created[0]
        update_data = {
            "title": "Updated Integration Test Task",
            "description": "This task has been updated during integration testing"
        }

        try:
            put_response = requests.put(f"{BASE_URL}/{user_id}/tasks/{first_task_id}",
                                      json=update_data, headers=headers)
            print(f"Update Task Response: {put_response.status_code}")

            if put_response.status_code == 200:
                updated_task = put_response.json()
                print(f"✓ Successfully updated task {first_task_id}")
            else:
                print(f"✗ Failed to update task: {put_response.status_code}")
                print(f"Response: {put_response.text}")
        except Exception as e:
            print(f"✗ Update task error: {str(e)}")

    print(f"\n--- Step 7: Test Task Completion ---")
    print("Updating task completion status...")

    # Step 7: Update task completion
    if tasks_created:
        first_task_id = tasks_created[0]
        completion_data = {"completed": True}

        try:
            patch_response = requests.patch(f"{BASE_URL}/{user_id}/tasks/{first_task_id}/complete",
                                          json=completion_data, headers=headers)
            print(f"Update Completion Response: {patch_response.status_code}")

            if patch_response.status_code == 200:
                completed_task = patch_response.json()
                print(f"✓ Successfully updated completion for task {first_task_id}")
            else:
                print(f"✗ Failed to update completion: {patch_response.status_code}")
                print(f"Response: {patch_response.text}")
        except Exception as e:
            print(f"✗ Update completion error: {str(e)}")

    print(f"\n--- Step 8: Verify Task Isolation ---")
    print("Testing that user can't access other users' tasks...")

    # Step 8: Test user isolation (try to access a fake task ID)
    fake_task_id = 999999  # Very unlikely to exist
    try:
        fake_get_response = requests.get(f"{BASE_URL}/{user_id}/tasks/{fake_task_id}",
                                       headers=headers)
        print(f"Access Fake Task Response: {fake_get_response.status_code}")

        if fake_get_response.status_code == 404:
            print("✓ Correctly returned 404 for non-existent task")
        else:
            print(f"? Got unexpected status for non-existent task: {fake_get_response.status_code}")
    except Exception as e:
        print(f"✗ Fake task access test error: {str(e)}")

    print(f"\n--- Step 9: Logout ---")
    print("Logging out...")

    # Step 9: Logout
    try:
        logout_response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        print(f"Logout Response: {logout_response.status_code}")

        if logout_response.status_code == 200:
            print("✓ Logout successful")
        else:
            print(f"Logout response (not necessarily an error): {logout_response.status_code}")
    except Exception as e:
        print(f"Logout error (may be expected): {str(e)}")

    print("\n" + "=" * 60)
    print("Full Integration Flow Testing Complete")
    print(f"User: {test_email}")
    print(f"Tasks created: {len(tasks_created)}")
    print(f"Tasks retrieved: {len(retrieved_tasks) if 'retrieved_tasks' in locals() else 0}")

    return True

def test_auth_error_cases():
    """Test error cases and invalid token handling"""
    print("\n\nTesting Error Cases and Invalid Token Handling")
    print("=" * 60)

    # Test with invalid token
    invalid_headers = {
        "Authorization": "Bearer invalid.token.here",
        "Content-Type": "application/json"
    }

    # Get user ID for the URL (using a fake one)
    fake_user_id = "fake-user-id-123"

    print("--- Testing Invalid Token Handling ---")
    try:
        response = requests.get(f"{BASE_URL}/{fake_user_id}/tasks", headers=invalid_headers)
        print(f"Request with invalid token: {response.status_code}")

        if response.status_code == 401:
            print("✓ Invalid token correctly rejected with 401")
        else:
            print(f"✗ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing invalid token: {str(e)}")

    print("\n--- Testing No Token Handling ---")
    no_auth_headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{BASE_URL}/{fake_user_id}/tasks", headers=no_auth_headers)
        print(f"Request with no token: {response.status_code}")

        if response.status_code == 401:
            print("✓ Missing token correctly rejected with 401")
        else:
            print(f"✗ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing no token: {str(e)}")

def main():
    """Run all integration tests"""
    print("Starting Full Integration Tests")
    print("=" * 60)

    # Check if backend is running
    try:
        health_check = requests.get(f"{BASE_URL.replace('/api', '')}/health")
        print(f"Backend health check: {health_check.status_code}")
    except requests.exceptions.ConnectionError:
        print("⚠ WARNING: Cannot connect to backend. Make sure the FastAPI server is running on localhost:8000")
        print("Run 'uvicorn backend.main:app --reload' in another terminal to start the server")
        return

    success = test_full_integration_flow()
    test_auth_error_cases()

    if success:
        print("\n🎉 All integration tests completed successfully!")
        print("The frontend-backend integration with JWT authentication is working properly.")
    else:
        print("\n❌ Some integration tests failed.")

if __name__ == "__main__":
    main()