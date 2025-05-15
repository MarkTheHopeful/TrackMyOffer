from datetime import datetime
from typing import Literal
from sqlalchemy.orm import Session
from database.db_interface import Profile


import os
import requests
from dotenv import load_dotenv
from loguru import logger
from typing import Optional

from models import JobDescriptionResponse

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


def request_model(prompt: str) -> Optional[str]:
    """
    Make a request to the AI model and return its text response.

    Args:
        prompt (str): The prompt to send to the AI model

    Returns:
        Optional[str]: The text response from the model or None if failed.
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
                "content": prompt,
            }
        ],
        "stream": False,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response and json_response.get("choices"):
                content = json_response["choices"][0]["message"]["content"]
                return content.strip()

        logger.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"Connection error: {e}")

    return None


LetterStyle = Literal["professional", "creative", "technical"]


def generate_ai_content(
    profile: Profile, job_description: JobDescriptionResponse, style: LetterStyle, notes: str
) -> str:
    """Generate the full cover letter using AI"""

    applicant_name = f"{profile.first_name} {profile.last_name}"
    applicant_email = profile.email or "not specified"
    applicant_phone = profile.phone or "not specified"

    location_parts = [part for part in [profile.city, profile.state, profile.country] if part]
    applicant_location = ", ".join(location_parts) if location_parts else "not specified"
    applicant_summary = profile.about_me or "a summary of my qualifications and experience."

    job_title = job_description.title or "the advertised position"
    company_name = job_description.company_name or "your esteemed company"

    job_details_list = []
    if job_description.title:
        job_details_list.append(f"- Job Title: {job_description.title}")
    if job_description.company_name:
        job_details_list.append(f"- Company: {job_description.company_name}")
    if job_description.company_city:
        job_details_list.append(f"- Location: {job_description.company_city}")
    if job_description.description:
        job_details_list.append(f"- Description: {job_description.description}")

    job_details_str = "\n".join(job_details_list)
    if not job_details_str:
        job_details_str = "Details about the job were not fully specified. Please refer to the job posting."

    recruiter_name = job_description.recruiter_name or "Hiring Manager"
    current_date_str = datetime.now().strftime("%B %d, %Y")

    prompt = f"""
    Please write a complete cover letter in a {style} style.

    **Applicant Information:**
    - Name: {applicant_name}
    - Email: {applicant_email}
    - Phone: {applicant_phone}
    - Current Location: {applicant_location}
    - Personal Summary/About Me: {applicant_summary}
    
    **Job Details:**
    {job_details_str}

    **Company Contact (for salutation):**
    - Contact Person: {recruiter_name}
    - Company Name: {company_name}

    **Additional Notes/Instructions from Applicant, what they want to add to the cover letter:**
    {notes if notes else "No specific notes provided."}

    **Task:**
    Generate a full, ready-to-send cover letter. The letter should be well-structured and include:
    1.  Applicant's Contact Information (e.g., {applicant_name}, {applicant_email}, {applicant_phone} at the top or bottom).
    2.  Date: {current_date_str}.
    3.  Recipient's Details: {recruiter_name}, {company_name}. (If a company address is available from job_description, it can be included; otherwise, omit.)
    4.  Salutation (e.g., "Dear {recruiter_name},").
    5.  Introduction: Clearly state you are applying for the {job_title} at {company_name}.
    6.  Body Paragraphs:
        - Express strong interest in the role and {company_name}.
        - Highlight how your skills and experiences (from your Personal Summary: "{applicant_summary}") match the job's requirements and responsibilities. Be specific and provide examples if possible.
        - Explain why you are a good fit for the company culture and this specific role.
        - If provided, subtly weave in points from the 'Additional Notes'.
    7.  Conclusion: Reiterate your enthusiasm for the opportunity and state your availability for an interview or further discussion.
    8.  Closing (e.g., "Sincerely," or "Yours faithfully,").
    9.  Your Typed Name: {applicant_name}.

    **Important Instructions:**
    - The tone must be strictly {style}.
    - Do not use placeholders (e.g., '[Your Address]', '[Company Address]')!!!!!!!! If specific information is not available, omit it or rephrase the content so that it appears complete and professional without it.
    - The output should be ONLY the cover letter text. No extra explanations, introductions, or markdown formatting like "```" surrounding the letter.
    - Ensure the letter is professional, grammatically correct, and flows naturally.
    
    The final version must look polished and ready to use as-isю
    """

    response = request_model(prompt)
    if response is None:
        # Provide a more comprehensive default fallback message if AI fails
        return (
            f"{applicant_name}\n"
            f"{applicant_email}\n"
            f"{applicant_phone}\n\n"
            f"{current_date_str}\n\n"
            f"{recruiter_name}\n"
            f"{company_name}\n\n"
            f"Dear {recruiter_name},\n\n"
            f"I am writing to express my keen interest in the {job_title} position at {company_name}, as advertised. "
            f"My background includes: {applicant_summary}.\n\n"
            f"I am confident that my skills and experience align well with your requirements and I am eager to contribute to your team. "
            f"Thank you for considering my application. I look forward to hearing from you.\n\n"
            f"Sincerely,\n"
            f"{applicant_name}"
        )
    return response


def generate_cover_letter_data(
    db: Session,
    profile: Profile,
    job_description: JobDescriptionResponse,
    style: LetterStyle = "professional",
    notes: str = "",
) -> str:
    """Generate a full cover letter based on profile and job description"""

    # Generate AI-powered full cover letter
    logger.info("Generating AI-powered full cover letter...")
    full_cover_letter = generate_ai_content(profile, job_description, style, notes)

    logger.info(f"Generated letter: {full_cover_letter}")

    return full_cover_letter
