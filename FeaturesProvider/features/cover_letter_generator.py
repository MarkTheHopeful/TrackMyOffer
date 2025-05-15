import json
from datetime import datetime
from typing import Literal, TypedDict

from database.db_interface import Profile
from loguru import logger
from models import JobDescriptionResponse
from sqlalchemy.orm import Session

from .ai_api import request_model


def parse_model_output(content: str) -> dict[str, str]:
    """
    Make a request to the AI model and return structured response

    Args:
        prompt (str): The prompt to send to the AI model

    Returns:
        Optional[Dict[str, str]]: Dictionary containing the structured response or None if failed
    """

    content = content.replace("```json", "").replace("```", "").strip()

    # Parse the content as JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse AI response as JSON: {content}")
        # Fallback to simple text splitting
        return {
            "why_interested": content[:200],
            "achievements": content[200:400],
            "why_good_fit": content[400:600],
        }


LetterStyle = Literal["professional", "creative", "technical"]


class CoverLetterData(TypedDict):
    current_date: str
    company_name: str
    company_address: str
    company_city: str
    company_postal_code: str
    recruiter_name: str
    job_title: str
    why_interested: str
    current_position_description: str
    key_achievements: str
    technical_skills_description: str
    why_good_candidate: str
    applicant_full_name: str
    applicant_phone: str
    applicant_email: str


def generate_ai_content(
    profile: Profile, job_description: JobDescriptionResponse, style: LetterStyle, notes: str
) -> dict[str, str]:
    """Generate AI-powered content for the cover letter"""
    prompt = f"""
    Generate content for a cover letter in {style} style.
    
    About the candidate:
    - Name: {profile.first_name} {profile.last_name}
    - Summary: {profile.about_me}
    - Location: {profile.city}, {profile.state}, {profile.country}
    
    For the job:
    {job_description}
    
    Use the following notes as a possible motivation source: {notes}
    
    Generate:
    1. Why interested in company (2-3 sentences)
    2. Key achievements description (2-3 sentences)
    3. Why good candidate (2-3 sentences)
        
    Please provide response in JSON format with keys: 'why_interested', 'achievements', 'why_good_fit'. Do not include markdown formatting.
    """

    output = request_model(prompt)
    if output is None:
        # Provide default response if AI fails
        return {
            "why_interested": "I am very interested in joining your company and contributing to its success.",
            "achievements": "Throughout my career, I have successfully delivered multiple projects.",
            "why_good_fit": "My skills and experience make me an excellent candidate for this position.",
        }

    parsed_output = parse_model_output(output)
    return parsed_output


def generate_cover_letter_data(
    db: Session,
    profile_id: int,
    job_description: JobDescriptionResponse,
    style: LetterStyle = "professional",
    notes: str = "",
) -> CoverLetterData:
    """Generate data for cover letter template based on profile and job description"""

    profile = db.query(Profile).filter_by(id=profile_id).first()
    if not profile:
        raise ValueError("Profile not found")

    # Generate AI-powered content
    ai_response = generate_ai_content(profile, job_description, style, notes)

    logger.info("Prepare first part of cover letter")
    # Prepare company-related data
    company_data = {
        "company_name": job_description.company_name,
        "company_address": job_description.company_address,
        "company_city": job_description.company_city,
        "company_postal_code": job_description.company_postal_code,
        "recruiter_name": job_description.recruiter_name,
        "job_title": job_description.title,
        "why_interested": ai_response.get("why_interested", "{NONE}"),
        "key_achievements": ai_response.get("achievements", "{NONE}"),
        "why_good_candidate": ai_response.get("why_good_fit", "{NONE}"),
    }

    logger.info("Prepare second part of cover letter")
    # Prepare applicant data
    applicant_data = {
        "applicant_full_name": f"{profile.first_name} {profile.last_name}",
        "applicant_phone": profile.phone or "",
        "applicant_email": profile.email or "",
        "current_position_description": profile.about_me or "",
        "technical_skills_description": "I have extensive experience in...",
    }

    logger.info("Combine data")
    # Combine all data into cover letter structure
    cover_letter_data = CoverLetterData(
        current_date=datetime.now().strftime("%B %d, %Y"),
        **company_data,
        **applicant_data,
    )

    return cover_letter_data


def fill_template(template: str, data: CoverLetterData) -> str:
    """Fill the template with the provided data"""
    return template.format(**data)
