# test_experience_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from datetime import date

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_experience_data():
    return {
        "profile_id": 1,
        "job_title": "Software Engineer",
        "company": "Tech Company",
        "start_date": "2020-01-01",
        "end_date": "2022-12-31",
        "description": "Developed web applications using Python and JavaScript"
    }

@pytest.fixture
def mock_db_experience():
    # Create a mock experience object that would be returned from the database
    experience = MagicMock()
    experience.id = 1
    experience.profile_id = 1
    experience.job_title = "Software Engineer"
    experience.company = "Tech Company"
    experience.start_date = date(2020, 1, 1)
    experience.end_date = date(2022, 12, 31)
    experience.description = "Developed web applications using Python and JavaScript"
    return experience

def test_create_experience(client, mock_experience_data, mock_db_experience):
    # Mock the database operations
    with patch("main.db_manager.get_profile", return_value=MagicMock()) as mock_get_profile, \
         patch("main.db_manager.add_experience", return_value=mock_db_experience) as mock_add_experience:
        
        # Send request to create a new experience
        response = client.post("/api/experience", json=mock_experience_data)
        
        # Verify the response
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["profile_id"] == 1
        assert response.json()["job_title"] == "Software Engineer"
        assert response.json()["company"] == "Tech Company"
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()
        mock_add_experience.assert_called_once()

def test_create_experience_profile_not_found(client, mock_experience_data):
    # Mock the database operations - profile not found
    with patch("main.db_manager.get_profile", return_value=None) as mock_get_profile:
        
        # Send request to create a new experience for non-existent profile
        response = client.post("/api/experience", json=mock_experience_data)
        
        # Verify error response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()

def test_get_experiences(client, mock_db_experience):
    # Mock the database operations
    with patch("main.db_manager.get_profile", return_value=MagicMock()) as mock_get_profile, \
         patch("main.db_manager.get_experiences", return_value=[mock_db_experience]) as mock_get_experiences:
        
        # Send request to get experiences for a profile
        response = client.get("/api/1/experiences")
        
        # Verify the response
        assert response.status_code == 200
        experiences = response.json()
        assert len(experiences) == 1
        assert experiences[0]["id"] == 1
        assert experiences[0]["job_title"] == "Software Engineer"
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()
        mock_get_experiences.assert_called_once()

def test_get_experiences_profile_not_found(client):
    # Mock the database operations - profile not found
    with patch("main.db_manager.get_profile", return_value=None) as mock_get_profile:
        
        # Send request to get experiences for non-existent profile
        response = client.get("/api/999/experiences")
        
        # Verify error response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
        # Verify the database operations were called correctly
        mock_get_profile.assert_called_once()