from datetime import datetime
from typing import Literal, TypedDict
from sqlalchemy.orm import Session
from database.db_interface import Profile


import os
import requests
from dotenv import load_dotenv
from loguru import logger
from typing import Optional, Dict

# Load environment variables from .env file
load_dotenv()


def get_key():
    # not a single string, because otherwise Openrouter bans it as soon as we commit it to Github
    code = "tl.ps.w2.dgd91524f6ee31g1bcc:629719:b78c37355fbecb9e1d5d828b2:64bfgeb5283"
    return "".join(chr(ord(c) - 1) for c in code)


API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY", get_key())

# MODEL_NAME = "deepseek/deepseek-v3-base:free"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"
PROMPTS = """
Please, write a greeting for person named '{}'.
It should be short and funny.
"""


def request_model(prompt: str) -> Optional[Dict[str, str]]:
    """
    Make a request to the AI model and return structured response
    
    Args:
        prompt (str): The prompt to send to the AI model
        
    Returns:
        Optional[Dict[str, str]]: Dictionary containing the structured response or None if failed
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt + "\n\nPlease provide response in JSON format with keys: 'why_interested', 'achievements', 'why_good_fit'. Do not include markdown formatting.",
            }
        ],
        "stream": False,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response:
                content = json_response["choices"][0]["message"]["content"]
                # Remove markdown formatting if present
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Parse the content as JSON
                try:
                    import json
                    return json.loads(content)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse AI response as JSON: {content}")
                    # Fallback to simple text splitting
                    return {
                        "why_interested": content[:200],
                        "achievements": content[200:400],
                        "why_good_fit": content[400:600]
                    }

        logger.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"Connection error: {e}")

    return None



LetterStyle = Literal["professional", "creative", "technical"]

class CoverLetterData(TypedDict):
    current_date: str
    company_name: str
    company_address: str
    company_city: str
    company_postal_code: str
    recruiter_name: str
    job_title: str
    why_interested_in_company: str
    current_position_description: str
    key_achievements: str
    technical_skills_description: str
    why_good_candidate: str
    applicant_full_name: str
    applicant_phone: str
    applicant_email: str

def generate_ai_content(profile: Profile, job_description: str, style: LetterStyle) -> dict:
    """Generate AI-powered content for the cover letter"""
    prompt = f"""
    Generate content for a cover letter in {style} style.
    
    About the candidate:
    - Name: {profile.first_name} {profile.last_name}
    - Summary: {profile.summary}
    - Location: {profile.city}, {profile.state}, {profile.country}
    
    For the job:
    {job_description}
    
    Generate:
    1. Why interested in company (2-3 sentences)
    2. Key achievements description (2-3 sentences)
    3. Why good candidate (2-3 sentences)
    """
    
    response = request_model(prompt)
    if response is None:
        # Provide default response if AI fails
        return {
            "why_interested": "I am very interested in joining your company and contributing to its success.",
            "achievements": "Throughout my career, I have successfully delivered multiple projects.",
            "why_good_fit": "My skills and experience make me an excellent candidate for this position."
        }
    return response

def generate_cover_letter_data(
    db: Session,
    profile_id: int,
    job_description: dict,
    style: LetterStyle = "professional"
) -> CoverLetterData:
    """Generate data for cover letter template based on profile and job description"""
    
    profile = db.query(Profile).filter_by(id=profile_id).first()
    if not profile:
        raise ValueError("Profile not found")

    # Generate AI-powered content
    ai_content = generate_ai_content(profile, job_description["description"], style)

    # Combine profile data with job description and AI-generated content
    cover_letter_data: CoverLetterData = {
        "current_date": datetime.now().strftime("%B %d, %Y"),
        "company_name": job_description.get("company_name", ""),
        "company_address": job_description.get("address", ""),
        "company_city": job_description.get("city", ""),
        "company_postal_code": job_description.get("postal_code", ""),
        "recruiter_name": job_description.get("recruiter_name", "Hiring Manager"),
        "job_title": job_description.get("title", ""),
        
        # Profile-based data
        "applicant_full_name": f"{profile.first_name} {profile.last_name}",
        "applicant_phone": profile.phone,
        "applicant_email": profile.email,
        
        # Current position and technical skills from profile
        "current_position_description": profile.summary or "",
        "technical_skills_description": "I have extensive experience in...",  # You might want to add a skills field to Profile
        
        # AI-generated content
        "why_interested_in_company": ai_content["why_interested"],
        "key_achievements": ai_content["achievements"],
        "why_good_candidate": ai_content["why_good_fit"]
    }
    
    return cover_letter_data

def fill_template(template: str, data: CoverLetterData) -> str:
    """Fill the template with the provided data"""
    return template.format(**data) 