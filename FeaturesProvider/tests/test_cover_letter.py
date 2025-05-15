import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from database.db_interface import Profile, DatabaseManager
from features.cover_letter_generator import generate_cover_letter_data, generate_ai_content
from models import JobDescriptionResponse

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
        about_me="Experienced software developer with 5 years of experience."
    )
    db.add(profile)
    db.commit()
    return profile

@pytest.fixture
def sample_job_description_model():
    return JobDescriptionResponse(
        company_name="Tech Corp",
        title="Senior Developer",
        description="Looking for an experienced developer...",
        recruiter_name="Jane Smith",
        location="San Francisco, CA",
        requirements="Python, FastAPI",
        responsibilities="Develop amazing things"
    )

def test_generate_ai_content(sample_profile, sample_job_description_model):
    with patch('features.cover_letter_generator.request_model') as mock_request:
        mock_full_letter = "Dear Jane Smith, I am John Doe... Sincerely, John Doe."
        mock_request.return_value = mock_full_letter

        result = generate_ai_content(
            sample_profile,
            sample_job_description_model,
            "professional",
            notes="Some specific notes."
        )

        assert result == mock_full_letter
        mock_request.assert_called_once()

def test_generate_ai_content_fallback(sample_profile, sample_job_description_model):
    with patch('features.cover_letter_generator.request_model', return_value=None):
        result = generate_ai_content(
            sample_profile,
            sample_job_description_model,
            "professional",
            notes=""
        )

        assert "John Doe" in result
        assert "john@example.com" in result
        assert "Tech Corp" in result
        assert "Senior Developer" in result
        assert "Sincerely," in result
        assert "My background includes: Experienced software developer with 5 years of experience." in result

def test_generate_cover_letter_data(db: Session, sample_profile, sample_job_description_model):
    with patch('features.cover_letter_generator.request_model') as mock_request:
        mock_ai_response_letter = (
            f"Dear Jane Smith,\n\n"
            f"I am writing to express my interest in the Senior Developer position at Tech Corp. "
            f"My name is John Doe and I am an Experienced software developer with 5 years of experience.\n\n"
            f"I am excited about this opportunity.\n\n"
            f"Sincerely,\nJohn Doe"
        )
        mock_request.return_value = mock_ai_response_letter

        full_letter = generate_cover_letter_data(
            db,
            sample_profile.id,
            sample_job_description_model,
            style="professional",
            notes="Please highlight my Python skills."
        )

        assert isinstance(full_letter, str)
        assert "Tech Corp" in full_letter
        assert "Senior Developer" in full_letter
        assert "John Doe" in full_letter
        assert "john@example.com" in full_letter
        assert mock_ai_response_letter == full_letter

        mock_request.assert_called_once()
        prompt_sent_to_ai = mock_request.call_args[0][0]
        assert "John Doe" in prompt_sent_to_ai
        assert "Tech Corp" in prompt_sent_to_ai
        assert "Please highlight my Python skills." in prompt_sent_to_ai
        assert "Experienced software developer with 5 years of experience." in prompt_sent_to_ai

def test_generate_cover_letter_invalid_profile(db: Session, sample_job_description_model):
    with pytest.raises(ValueError, match="Profile not found"):
        generate_cover_letter_data(db, 999, sample_job_description_model)

@pytest.mark.integration
def test_ai_request_model():
    """Integration test for AI model request to generate a full letter."""
    from features.cover_letter_generator import request_model
    
    test_prompt = """
    Please write a complete cover letter in a professional style.

    **Applicant Information:**
    - Name: Test User
    - Email: test@example.com
    - Phone: 555-1234
    - Current Location: Testville, TS
    - Personal Summary/About Me: A dedicated professional seeking new opportunities.
    
    **Job Details:**
    - Job Title: Sample Role
    - Company: Sample Company Inc.
    - Description: A great job.
    - Key Requirements: Enthusiasm.

    **Company Contact (for salutation):**
    - Contact Person: Hiring Team
    - Company Name: Sample Company Inc.

    **Additional Notes/Instructions from Applicant:**
    Keep it concise.

    **Task:**
    Generate a full, ready-to-send cover letter.
    The output should be ONLY the cover letter text. No extra explanations.
    """
    
    response = request_model(test_prompt)
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response.strip()) > 50
    assert "Test User" in response or "Sample Role" in response

    assert len(response) > 50