import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from models import ProfileCreate, ProfileResponse
from datetime import datetime


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_profile_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "city": "New York",
        "state": "NY",
        "country": "USA",
        "summary": "Experienced software developer"
    }


@pytest.fixture
def mock_db_profile():
    # Create a mock profile object that would be returned from the database
    profile = MagicMock()
    profile.id = 1
    profile.first_name = "John"
    profile.last_name = "Doe"
    profile.email = "john.doe@example.com"
    profile.phone = "1234567890"
    profile.city = "New York"
    profile.state = "NY"
    profile.country = "USA"
    profile.summary = "Experienced software developer"
    profile.created_at = datetime.utcnow()
    profile.updated_at = datetime.utcnow()
    return profile


def test_create_profile(client, mock_profile_data, mock_db_profile):
    # Mock the database operations
    with patch("main.db_manager.get_profile_by_email", return_value=None) as mock_get_profile, \
         patch("main.db_manager.add_profile", return_value=mock_db_profile) as mock_add_profile:
        
        # Send request to create a new profile
        response = client.post("/api/profile", json=mock_profile_data)
        
        # Verify the response
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["first_name"] == "John"
        assert response.json()["last_name"] == "Doe"
        assert response.json()["email"] == "john.doe@example.com"
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()
        mock_add_profile.assert_called_once()


def test_update_profile(client, mock_profile_data, mock_db_profile):
    # Mock the database operations
    with patch("main.db_manager.get_profile_by_email", return_value=mock_db_profile) as mock_get_profile, \
         patch("main.db_manager.update_profile", return_value=mock_db_profile) as mock_update_profile:
        
        # Send request to update an existing profile
        response = client.post("/api/profile", json=mock_profile_data)
        
        # Verify the response
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["first_name"] == "John"
        assert response.json()["email"] == "john.doe@example.com"
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()
        mock_update_profile.assert_called_once()


def test_create_profile_validation_error(client):
    # Test with missing required fields
    invalid_data = {
        "first_name": "John",
        # Missing last_name and other required fields
        "email": "john.doe@example.com"
    }
    
    response = client.post("/api/profile", json=invalid_data)
    
    # Verify validation error response
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_profile_with_invalid_email(client):
    # Test with invalid email format
    invalid_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",  # Invalid email format
        "city": "New York",
        "state": "NY",
        "country": "USA"
    }
    
    response = client.post("/api/profile", json=invalid_data)
    
    # Verify validation error response
    assert response.status_code == 422
    assert "detail" in response.json()
    # Check that the error is related to the email field
    errors = response.json()["detail"]
    assert any(error["loc"][1] == "email" for error in errors) 
    