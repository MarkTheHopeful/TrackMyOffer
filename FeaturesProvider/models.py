from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import date


class ProfileCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    summary: Optional[str] = None


class EducationCreate(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: Optional[date] = None
    additional_info: Optional[str] = None


class SocialMediaCreate(BaseModel):
    linkedin_url: Optional[str] = Field(None, max_length=255)
    github_url: Optional[str] = Field(None, max_length=255)
    personal_website: Optional[str] = Field(None, max_length=255)
    other_links: Optional[Dict[str, str]] = None


class ProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    city: str
    state: str
    country: str
    summary: Optional[str] = None
    
    class Config:
        from_attributes = True


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

    class Config:
        orm_mode = True
