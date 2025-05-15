import pytest
from datetime import date
from database.db_interface import DatabaseManager, Education


@pytest.fixture
def db_manager():
    """Create a database manager instance for testing"""
    manager = DatabaseManager(test_mode=True)  # Use SQLite in-memory database
    manager.create_tables()
    return manager


@pytest.fixture
def sample_profile_data():
    """Sample profile data for testing"""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "city": "New York",
        "state": "NY",
        "country": "USA",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "github_url": "https://github.com/johndoe",
        "personal_website": "https://johndoe.com",
        "other_url": "https://twitter.com/johndoe",
        "about_me": "Software Engineer with 5 years of experience",
    }


@pytest.fixture
def sample_experience_data():
    """Sample experience data for testing"""
    return {
        "job_title": "Senior Software Engineer",
        "company": "Tech Corp",
        "start_date": date(2018, 1, 1),
        "end_date": date(2023, 12, 31),
        "description": "Led development of multiple full-stack applications",
    }


@pytest.fixture
def sample_education_data():
    """Sample education data for testing"""
    return {
        "institution": "University of Example",
        "degree": "Computer Science",
        "start_date": date(2018, 9, 1),
        "end_date": date(2022, 5, 1),
        "additional_info": "Graduated with honors",
    }


@pytest.fixture
def sample_social_media_data():
    """Sample social media data for testing"""
    return {
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "github_url": "https://github.com/johndoe",
        "personal_website": "https://johndoe.com",
        "other_links": {"twitter": "https://twitter.com/johndoe"},
    }


def test_create_profile(db_manager, sample_profile_data):
    """Test creating a new profile"""
    session = db_manager.get_session()
    try:
        profile = db_manager.add_profile(session, sample_profile_data)
        assert profile.id is not None
        assert profile.first_name == sample_profile_data["first_name"]
        assert profile.last_name == sample_profile_data["last_name"]
        assert profile.email == sample_profile_data["email"]
        assert profile.phone == sample_profile_data["phone"]
        assert profile.city == sample_profile_data["city"]
        assert profile.state == sample_profile_data["state"]
        assert profile.country == sample_profile_data["country"]
        assert profile.about_me == sample_profile_data["about_me"]
        assert profile.created_at is not None
        assert profile.updated_at is not None
    finally:
        db_manager.close_session(session)


def test_get_profile(db_manager, sample_profile_data):
    """Test retrieving a profile"""
    session = db_manager.get_session()
    try:
        # Create a profile first
        profile = db_manager.add_profile(session, sample_profile_data)

        # Retrieve the profile
        retrieved_profile = db_manager.get_profile(session, profile.id)
        assert retrieved_profile is not None
        assert retrieved_profile.id == profile.id
        assert retrieved_profile.email == sample_profile_data["email"]
    finally:
        db_manager.close_session(session)


def test_get_profile_by_email(db_manager, sample_profile_data):
    """Test retrieving a profile by email"""
    session = db_manager.get_session()
    try:
        # Create a profile first
        profile = db_manager.add_profile(session, sample_profile_data)

        # Retrieve the profile by email
        retrieved_profile = db_manager.get_profile_by_email(session, sample_profile_data["email"])
        assert retrieved_profile is not None
        assert retrieved_profile.id == profile.id
        assert retrieved_profile.email == sample_profile_data["email"]
    finally:
        db_manager.close_session(session)


def test_update_profile(db_manager, sample_profile_data):
    """Test updating a profile"""
    session = db_manager.get_session()
    try:
        # Create a profile first
        profile = db_manager.add_profile(session, sample_profile_data)

        # Update the profile
        update_data = {"first_name": "Jane", "phone": "+1987654321", "about_me": "Updated about me"}
        updated_profile = db_manager.update_profile(session, profile.id, update_data)

        # Ensure the updated_profile is an object, not a boolean
        assert updated_profile is not None
        assert updated_profile.first_name == update_data["first_name"]
        assert updated_profile.phone == update_data["phone"]
        assert updated_profile.about_me == update_data["about_me"]
        assert updated_profile.last_name == sample_profile_data["last_name"]  # Unchanged field
    finally:
        db_manager.close_session(session)


def test_delete_profile(db_manager, sample_profile_data):
    """Test deleting a profile"""
    session = db_manager.get_session()
    try:
        # Create a profile first
        profile = db_manager.add_profile(session, sample_profile_data)

        # Delete the profile
        result = db_manager.delete_profile(session, profile.id)
        assert result is True

        # Verify the profile is deleted
        deleted_profile = db_manager.get_profile(session, profile.id)
        assert deleted_profile is None
    finally:
        db_manager.close_session(session)


def test_add_education(db_manager, sample_profile_data, sample_education_data):
    """Test adding education to a profile"""
    session = db_manager.get_session()
    try:
        # Create a profile first
        profile = db_manager.add_profile(session, sample_profile_data)

        # Add education
        education = db_manager.add_education(session, profile.id, sample_education_data)

        assert education.id is not None
        assert education.profile_id == profile.id
        assert education.institution == sample_education_data["institution"]
        assert education.degree == sample_education_data["degree"]
        assert education.start_date == sample_education_data["start_date"]
        assert education.end_date == sample_education_data["end_date"]
        assert education.additional_info == sample_education_data["additional_info"]
    finally:
        db_manager.close_session(session)


def test_profile_relationships(db_manager, sample_profile_data, sample_education_data, sample_social_media_data):
    """Test relationships between profile, education, and social media"""
    session = db_manager.get_session()
    try:
        # Create a profile
        profile = db_manager.add_profile(session, sample_profile_data)

        # Add education
        education = db_manager.add_education(session, profile.id, sample_education_data)

        # Test relationships
        assert len(profile.education) == 1
        assert profile.education[0].id == education.id

        # Test cascade delete
        db_manager.delete_profile(session, profile.id)
        assert db_manager.get_profile(session, profile.id) is None
        assert session.query(Education).filter_by(id=education.id).first() is None
    finally:
        db_manager.close_session(session)
