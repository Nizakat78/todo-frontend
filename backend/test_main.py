import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

def test_api_without_auth():
    """Test that API endpoints require authentication"""
    # This test will fail until we implement proper testing with mocked authentication
    # For now, this is a placeholder to show the test structure
    pass