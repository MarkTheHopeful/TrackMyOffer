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
        "company_city": "San Francisco",
        "company_address": "123 Tech Street",
        "company_postal_code": "94105",
        "title": "Senior Developer",
        "description": "Looking for an experienced developer...",
        "recruiter_name": "Jane Smith",
    }

    # Mock the AI response for cover letter generation
    mock_ai_response = f"""
    SOME COVER LETTER...
    {job_description["company_name"]},
    {job_description["company_city"]},
    {job_description["company_address"]},
    {job_description["company_postal_code"]},
    {job_description["title"]},
    {job_description["description"]},
    {job_description["recruiter_name"]}
    """

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

        data = response.json()
        assert data["cover_letter"] == mock_ai_response


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
