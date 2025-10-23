from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import date


class ProfileCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = Field(None, max_length=255)
    github_url: Optional[str] = Field(None, max_length=255)
    personal_website: Optional[str] = Field(None, max_length=255)
    other_url: Optional[str] = Field(None, max_length=255)
    about_me: Optional[str] = Field(None)


class ProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    personal_website: Optional[str] = None
    other_url: Optional[str] = None
    about_me: Optional[str] = None

    model_config = {"from_attributes": True}


class EducationCreate(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: Optional[date] = None
    additional_info: Optional[str] = None


class EducationResponse(BaseModel):
    id: int
    institution: str
    degree: str
    start_date: date
    end_date: Optional[date] = None
    additional_info: Optional[str] = None


class ExperienceCreate(BaseModel):
    profile_id: int
    job_title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None


class ExperienceResponse(BaseModel):
    id: int
    profile_id: int
    job_title: str
    company: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class JobDescriptionReceive(BaseModel):
    jobDescription: str


class JobDescriptionResponse(BaseModel):
    company_name: str
    company_address: str
    company_city: str
    company_postal_code: str
    recruiter_name: str
    title: str
    description: str


class GeneratedCV(BaseModel):
    format: str = "md"
    cv_text: str


class ReviewResponse(BaseModel):
    matchScore: int
    suggestions: List[str]


class AchievementsRewriteItem(BaseModel):
    original_achievement: str
    rewritten_achievement: str
    style: str


class AchievementsRewriteRequest(BaseModel):
    achievements: List[str]
    style: Optional[str] = "professional"
    context: Optional[str] = ""


class AchievementsRewriteResponse(BaseModel):
    results: List[AchievementsRewriteItem]
