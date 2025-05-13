from ai import request_model
from database.db_interface import DatabaseManager
from fastapi import Depends, FastAPI, HTTPException, status
from models import ProfileCreate, ProfileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from models import ExperienceCreate, ExperienceResponse
from features.cover_letter_generator import generate_cover_letter_data, fill_template
import os

app = FastAPI()

# Initialize database manager
db_manager = DatabaseManager()


# Create tables on startup
@app.on_event("startup")
def startup_event():
    db_manager.create_tables()


# Dependency to get database session
def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db_manager.close_session(db)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}


@app.post("/greet", status_code=status.HTTP_200_OK)
def greet(payload: dict[str, str]) -> dict[str, str]:
    name = payload.get("name")
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required"
        )

    greeting = request_model(name)
    if greeting is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable",
        )
    return {"message": greeting}


@app.get(
    "/api/profile/{profile_id}", response_model=ProfileResponse, status_code=status.HTTP_200_OK
)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get profile from the database by its id (numerical)
    If a profile does not exist, raise 404
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    return profile
@app.post(
    "/api/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED
)
def create_or_update_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """
    Create or update a user profile.
    If a profile with the given email already exists, it will be updated.
    Otherwise, a new profile will be created.
    """
    # Check if profile with this email already exists
    existing_profile = db_manager.get_profile_by_email(db, profile.email)

    if existing_profile:
        # Update existing profile
        updated_profile = db_manager.update_profile(
            db, existing_profile.id, profile.dict()
        )
        return updated_profile
    else:
        # Create new profile
        new_profile = db_manager.add_profile(db, profile.dict())
        return new_profile

@app.post("/api/experience", response_model=ExperienceResponse, status_code=201)
def create_experience(experience_data: ExperienceCreate, db: Session = Depends(get_db)):
    """Create a new experience entry for a profile"""
    # Check if the profile exists
    profile = db_manager.get_profile(db, experience_data.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {experience_data.profile_id} not found")

    # Convert pydantic model to dict
    experience_dict = experience_data.dict()

    # Add the experience to the database
    experience = db_manager.add_experience(db, profile.id, experience_dict)

    return experience

@app.get("/api/experiences/{profile_id}", response_model=List[ExperienceResponse])
def get_experiences(profile_id: int, db: Session = Depends(get_db)):
    """Get all experiences for a profile"""
    # Check if the profile exists
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")

    # Get experiences
    experiences = db_manager.get_experiences(db, profile_id)

    return experiences

@app.post("/api/generate-cover-letter")
def generate_cover_letter(
    profile_id: int,
    job_description: dict,
    style: str = "professional",
    db: Session = Depends(get_db)
):
    """Generate a cover letter based on profile and job description"""
    try:
        # Read the template file
        template_path = os.path.join("templates", "cover_letter_basic.txt")
        with open(template_path, "r") as f:
            template = f.read()

        # Generate data for the template
        letter_data = generate_cover_letter_data(db, profile_id, job_description, style)

        # Fill the template with the data
        filled_letter = fill_template(template, letter_data)

        return {
            "cover_letter": filled_letter,
            "data": letter_data
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
