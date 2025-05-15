import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from database.db_interface import Profile
from main import app
from sqlalchemy.orm import Session
from database.db_interface import DatabaseManager
from tests.test_profile_api import mock_db_profile


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db():
    # Use SQLite in-memory database for testing
    db_manager = DatabaseManager(test_mode=True)
    db_manager.create_tables()
    return db_manager.get_session()


def test_home_route(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


@pytest.mark.parametrize(
    "mock_return,payload,expected_status,expected_response",
    [
        ("Hello, John!", {"name": "John"}, 200, {"message": "Hello, John!"}),
        (None, {"name": "John"}, 503, {"detail": "AI service is currently unavailable"}),
        (None, {}, 400, {"detail": "Name is required"}),
    ],
)
def test_greet_route(
    client: TestClient,
    mock_return: str | None,
    payload: dict[str, str],
    expected_status: int,
    expected_response: dict[str, str],
) -> None:
    with patch("main.request_model", return_value=mock_return):
        response = client.post("/greet", json=payload)
        assert response.status_code == expected_status
        assert response.json() == expected_response


def test_generate_cover_letter_endpoint(client: TestClient, db: Session, mock_db_profile: Profile):
    # Test cover letter generation
    job_description = {
        "company_name": "Tech Corp",
        "title": "Senior Developer",
        "description": "Looking for an experienced developer...",
        "recruiter_name": "Jane Smith",
        "address": "123 Tech Street",
        "city": "San Francisco",
        "postal_code": "94105",
    }

    # Mock the AI response for cover letter generation
    mock_ai_response = {
        "why_interested": "Test interest",
        "achievements": "Test achievements",
        "why_good_fit": "Test fit",
    }

    with (
        patch("features.cover_letter_generator.request_model", return_value=mock_ai_response),
        patch("main.db_manager.get_profile", return_value=mock_db_profile),
    ):
        response = client.post(
            "/api/generate-cover-letter",
            params={"profile_id": "123", "style": "professional"},
            json=job_description,
        )

        assert response.status_code == 200
        assert "cover_letter" in response.json()
        assert "data" in response.json()

        data = response.json()["data"]
        assert data["company_name"] == "Tech Corp"
        assert data["applicant_full_name"] == "John Doe"
        assert data["why_interested_in_company"] == "Test interest"
        assert data["key_achievements"] == "Test achievements"
        assert data["why_good_candidate"] == "Test fit"


def test_generate_cover_letter_invalid_profile(client: TestClient, db: Session):
    job_description = {
        "company_name": "Tech Corp",
        "title": "Senior Developer",
        "description": "Looking for an experienced developer...",
    }

    response = client.post(
        "/api/generate-cover-letter", params={"profile_id": 999, "style": "professional"}, json=job_description
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
