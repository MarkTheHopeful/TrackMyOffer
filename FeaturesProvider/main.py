import os
from contextlib import asynccontextmanager
from typing import List

from database.db_interface import DatabaseManager
from fastapi import Depends, FastAPI, HTTPException, status
from features import (
    analyze_gaps,
    generate_cover_letter_data,
    job_description_from_text,
    md_cv_from_user_and_job,
    request_model,
    review_from_user_and_job,
    text_job_position_from_link,
)
from loguru import logger
from models import (
    EducationCreate,
    EducationResponse,
    ExperienceCreate,
    ExperienceResponse,
    GapAnalysisResponse,
    GeneratedCV,
    JobDescriptionReceive,
    JobDescriptionResponse,
    ProfileCreate,
    ProfileResponse,
    ReviewResponse,
)
from sqlalchemy.orm import Session

app = FastAPI()

# Initialize database manager
db_manager = DatabaseManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    testing = "PYTEST_CURRENT_TEST" in os.environ
    if not testing:
        logger.info("Creating database tables...")
        db_manager.create_tables()
        logger.info("Database tables created")

    yield None


app = FastAPI(lifespan=lifespan)


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")

    greeting = request_model(name)
    if greeting is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable",
        )
    return {"message": greeting}


@app.get("/api/profile/{profile_id}", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get profile from the database by its id (numerical)
    If a profile does not exist, raise 404
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    return profile


@app.post("/api/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
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
        updated_profile = db_manager.update_profile(db, existing_profile.id, profile.model_dump())
        return updated_profile
    else:
        # Create new profile
        new_profile = db_manager.add_profile(db, profile.model_dump())
        return new_profile


@app.post("/api/profile/{profile_id}/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
def create_education(profile_id: int, education: EducationCreate, db: Session = Depends(get_db)):
    """
    Create (insert) an education entry for the given profile id
    404 on an invalid profile id
    Otherwise a new education entry will be returned (with id given).
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    education = db_manager.add_education(db, profile_id, education.model_dump())
    return education


@app.delete("/api/profile/{profile_id}/education/{education_id}", status_code=status.HTTP_200_OK)
def delete_education(profile_id: int, education_id: int, db: Session = Depends(get_db)):
    """
    Delete education entry with given education_id and profile_id
    404 on an invalid education or profile id
    Otherwise 200
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    del_status = db_manager.delete_education(db, education_id)
    return del_status


@app.get("/api/{profile_id}/educations", response_model=List[EducationResponse])
def get_educations(profile_id: int, db: Session = Depends(get_db)):
    """Get all education entries for a profile"""
    # Check if the profile exists
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")

    # Get experiences
    educations = db_manager.get_educations(db, profile_id)

    return educations


@app.post("/api/experience", response_model=ExperienceResponse, status_code=201)
def create_experience(experience_data: ExperienceCreate, db: Session = Depends(get_db)):
    """Create a new experience entry for a profile"""
    # Check if the profile exists
    profile = db_manager.get_profile(db, experience_data.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {experience_data.profile_id} not found")

    # Convert pydantic model to dict
    experience_dict = experience_data.model_dump()

    # Add the experience to the database
    experience = db_manager.add_experience(db, profile.id, experience_dict)

    return experience


@app.delete("/api/{profile_id}/experiences/{experience_id}", status_code=status.HTTP_200_OK)
def delete_experience(profile_id: int, experience_id: int, db: Session = Depends(get_db)):
    """
    Delete experience entry with given experience_id and profile_id
    404 on an invalid experience or profile id
    Otherwise 200
    """
    # Check if the profile exists
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    del_status = db_manager.delete_experience(db, experience_id)
    return del_status


@app.get("/api/{profile_id}/experiences", response_model=List[ExperienceResponse])
def get_experiences(profile_id: int, db: Session = Depends(get_db)):
    """Get all experiences for a profile"""
    # Check if the profile exists
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")

    # Get experiences
    experiences = db_manager.get_experiences(db, profile_id)

    return experiences


@app.post("/api/extract-job-description", response_model=JobDescriptionResponse)
def extract_job_description(job_description_raw: JobDescriptionReceive):
    jd_text = job_description_raw.jobDescription
    if jd_text.startswith("https://") or jd_text.startswith("http://"):
        jd_text = text_job_position_from_link(jd_text)

    return job_description_from_text(jd_text)


@app.post("/api/build-cv", response_model=GeneratedCV)
def generate_cv(profile_id: int, job_description: JobDescriptionResponse, db: Session = Depends(get_db)):
    """
    Generates a tailored cv for a given user and job_description (already parsed)
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    educations = db_manager.get_educations(db, profile_id)
    experiences = db_manager.get_experiences(db, profile_id)
    return md_cv_from_user_and_job(profile, educations, experiences, job_description)


@app.post("/api/match-position", response_model=ReviewResponse)
async def review_cv(profile_id: int, job_description: JobDescriptionResponse, db: Session = Depends(get_db)):
    """
    Given profile id and job_description (already parsed),
    match given user against given job and evaluate the chances of passing.
    Does not accept actual CV file! Match is done against all the info we have about the user!
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    educations = db_manager.get_educations(db, profile_id)
    experiences = db_manager.get_experiences(db, profile_id)
    return review_from_user_and_job(profile, educations, experiences, job_description)


@app.post("/api/generate-cover-letter")
def generate_cover_letter(
    profile_id: int,
    job_description: JobDescriptionResponse,
    style: str = "professional",
    notes: str = "",
    db: Session = Depends(get_db),
):
    """Generate a cover letter based on profile and job description"""

    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")

    try:
        # The 'style' parameter is passed as a string.
        # The generate_cover_letter_data function expects LetterStyle,
        # but since it's used in an f-string for the prompt, direct string usage is acceptable here.
        # For more robust type safety, you could add validation for 'style' if needed.

        # Generate the full cover letter string
        full_cover_letter = generate_cover_letter_data(
            db,
            profile,
            job_description,
            style,  # type: ignore
            notes,
        )
        # Added type: ignore for style as generate_cover_letter_data expects LetterStyle
        # but we are passing a string. This is functionally fine for this use case.

        return {
            "cover_letter": full_cover_letter,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}", exc_info=True)  # Added exc_info for better logging
        raise HTTPException(status_code=500, detail="An unexpected error occurred while generating the cover letter.")

@app.delete("/api/profile/{profile_id}", status_code=status.HTTP_200_OK)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete profile with given profile_id
    404 on an invalid profile id
    Otherwise 200
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")
    del_status = db_manager.delete_profile(db, profile_id)
    return del_status
<<<<<<< HEAD

@app.post("/api/analyze-gaps", response_model=GapAnalysisResponse)
async def analyze_experience_gaps(
    profile_id: int,
    job_description: JobDescriptionResponse,
    db: Session = Depends(get_db)
):
    """
    Analyze gaps between candidate's profile and job requirements.
    Returns gaps categorized by severity: Critical, Important, Nice-to-have.

    Given profile id and job_description (already parsed),
    identify small experience or responsibility gaps where the candidate could add more information.
    """
    profile = db_manager.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {profile_id} not found")

    educations = db_manager.get_educations(db, profile_id)
    experiences = db_manager.get_experiences(db, profile_id)

    result = analyze_gaps(profile, educations, experiences, job_description)
    return result
=======
>>>>>>> 4e69cc4 ([Backend] exporting/deleting user info)
