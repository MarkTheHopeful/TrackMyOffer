from unittest.mock import patch

import pytest
from database.db_interface import DatabaseManager, Profile
from features.cover_letter_generator import fill_template, generate_ai_content, generate_cover_letter_data
from sqlalchemy.orm import Session


@pytest.fixture
def db():
    # Use SQLite in-memory database for testing
    db_manager = DatabaseManager(test_mode=True)
    db_manager.create_tables()
    return db_manager.get_session()


@pytest.fixture
def sample_profile(db: Session):
    profile = Profile(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        city="New York",
        state="NY",
        country="USA",
        summary="Experienced software developer with 5 years of experience",
    )
    db.add(profile)
    db.commit()
    return profile


@pytest.fixture
def sample_job_description():
    return {
        "company_name": "Tech Corp",
        "title": "Senior Developer",
        "description": "Looking for an experienced developer...",
        "recruiter_name": "Jane Smith",
        "address": "123 Tech Street",
        "city": "San Francisco",
        "postal_code": "94105",
    }


def test_generate_ai_content(sample_profile):
    with patch("features.cover_letter_generator.request_model") as mock_request:
        mock_response = {
            "why_interested": "Test interest",
            "achievements": "Test achievements",
            "why_good_fit": "Test fit",
        }
        mock_request.return_value = mock_response

        result = generate_ai_content(sample_profile, "Test job description", "professional")

        assert result == mock_response
        mock_request.assert_called_once()


def test_generate_ai_content_fallback(sample_profile):
    with patch("features.cover_letter_generator.request_model", return_value=None):
        result = generate_ai_content(sample_profile, "Test job description", "professional")

        assert "why_interested" in result
        assert "achievements" in result
        assert "why_good_fit" in result


def test_generate_cover_letter_data(db: Session, sample_profile, sample_job_description):
    with patch("features.cover_letter_generator.request_model") as mock_request:
        mock_response = {
            "why_interested": "Test interest",
            "achievements": "Test achievements",
            "why_good_fit": "Test fit",
        }
        mock_request.return_value = mock_response

        data = generate_cover_letter_data(db, sample_profile.id, sample_job_description)

        assert data["company_name"] == "Tech Corp"
        assert data["job_title"] == "Senior Developer"
        assert data["applicant_full_name"] == "John Doe"
        assert data["applicant_email"] == "john@example.com"
        assert data["why_interested"] == "Test interest"
        assert data["key_achievements"] == "Test achievements"
        assert data["why_good_candidate"] == "Test fit"


def test_fill_template():
    template = """
    Dear {recruiter_name},
    
    I am writing about {job_title} position at {company_name}.
    
    Best regards,
    {applicant_full_name}
    """

    data = {
        "recruiter_name": "Jane Smith",
        "job_title": "Senior Developer",
        "company_name": "Tech Corp",
        "applicant_full_name": "John Doe",
    }

    filled_letter = fill_template(template, data)

    assert "Dear Jane Smith" in filled_letter
    assert "Senior Developer position at Tech Corp" in filled_letter
    assert "John Doe" in filled_letter


def test_generate_cover_letter_invalid_profile(db: Session, sample_job_description):
    with pytest.raises(ValueError, match="Profile not found"):
        generate_cover_letter_data(db, 999, sample_job_description)


@pytest.mark.integration
def test_ai_request_model():
    """Integration test for AI model request"""
    from features.cover_letter_generator import request_model

    test_prompt = """
    Generate content for a cover letter in professional style.
    
    About the candidate:
    - Name: John Doe
    - Summary: Senior software developer with 10 years of experience
    - Location: New York, NY, USA
    
    For the job:
    Senior Developer position at Tech Corp
    
    Generate:
    1. Why interested in company (2-3 sentences)
    2. Key achievements description (2-3 sentences)
    3. Why good candidate (2-3 sentences)
    """

    response = request_model(test_prompt)

    assert response is not None
    assert isinstance(response, dict)
    assert all(key in response for key in ["why_interested", "achievements", "why_good_fit"])

    # Check that each response part is a non-empty string
    for key, value in response.items():
        assert isinstance(value, str)
        assert len(value.strip()) > 0

    # Check that responses are reasonable in length
    assert len(response["why_interested"]) > 50
    assert len(response["achievements"]) > 50
    assert len(response["why_good_fit"]) > 50
