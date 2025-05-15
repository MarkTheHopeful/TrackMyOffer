import os

import requests
from database.db_interface import Education, Experience, Profile
from dotenv import load_dotenv
from loguru import logger
from models import GeneratedCV, JobDescriptionResponse

from FeaturesProvider.features.review_user_application import _format_experience, _format_education
from FeaturesProvider.models import ReviewResponse

# Load environment variables from .env file
load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY")

# MODEL_NAME = "deepseek/deepseek-v3-base:free"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"


def request_model(prompt: str) -> str | None:
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
        response = requests.post(API_URL, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response:
                return json_response["choices"][0]["message"]["content"]

        logger.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"Connection error: {e}")

    return None


def _format_education_for_cv(educations: list[Education]) -> str:
    """Helper function to format education information for the CV prompt"""
    if not educations:
        return "No formal education provided"

    edu_text = []
    for edu in educations:
        end_date = edu.end_date.strftime("%Y-%m") if edu.end_date else "Present"
        edu_text.append(
            f"- {edu.institution}, {edu.degree}, {edu.start_date.strftime('%Y-%m')} to {end_date}"
            + (f", {edu.additional_info}" if edu.additional_info else "")
        )

    return "\n".join(edu_text)


def _format_experience_for_cv(experiences: list[Experience]) -> str:
    """Helper function to format experience information for the CV prompt"""
    if not experiences:
        return "No work experience provided"

    exp_text = []
    for exp in experiences:
        end_date = exp.end_date if exp.end_date else "Present"
        exp_text.append(
            f"- {exp.company}, {exp.job_title}, {exp.start_date} to {end_date}"
            + (f"\n  {exp.description}" if exp.description else "")
        )

    return "\n".join(exp_text)


def md_cv_from_user_and_job(
        profile: Profile,
        educations: list[Education],
        experiences: list[Experience],
        job_description: JobDescriptionResponse,
) -> GeneratedCV:
    """
    Given the full information about a user, generate a tailored markdown CV
    The provided information is:
    - profile description as present in the db
    - list of all user education entries
    - list of all user experience entries
    - job_description
    """
    # Create a comprehensive prompt for the AI model
    prompt = f"""
    Create a professional, tailored Markdown CV for a job application based on the following information:
    
    CANDIDATE INFORMATION:
    Full Name: {profile.first_name} {profile.last_name}
    Email: {profile.email}
    Location: {profile.city or ""}, {profile.state or ""}, {profile.country or ""}
    Phone: {profile.phone or "Not provided"}
    LinkedIn: {profile.linkedin_url or "Not provided"}
    GitHub: {profile.github_url or "Not provided"}
    Personal Website: {profile.personal_website or "Not provided"}
    Other URL: {profile.other_url or "Not provided"}
    About Me: {profile.about_me or "Not provided"}
    
    EDUCATION:
    {_format_education_for_cv(educations)}
    
    WORK EXPERIENCE:
    {_format_experience_for_cv(experiences)}
    
    TARGET JOB:
    Company: {job_description.company_name}
    Position: {job_description.title}
    Job Description: {job_description.description}
    
    INSTRUCTIONS:
    1. Create a professional-looking Markdown CV tailored specifically for this job position.
    2. Highlight skills and experiences that are most relevant to the job description.
    3. Structure the CV with clear headings (use Markdown formatting).
    4. Include all contact information in a professional header.
    5. Focus on achievements and quantifiable results in experience descriptions.
    6. Make sure the CV is well-organized and easy to read.
    7. Adapt the candidate's background to emphasize relevance to this specific job.
    
    RETURN ONLY THE MARKDOWN CV, without any explanations or additional text.
    """

    # Call the AI model
    cv_text = request_model(prompt)

    # Handle potential API failures
    if not cv_text:
        logger.warning("AI model failed to generate CV, using fallback template")
        # Provide a basic fallback template
        cv_text = f"""# {profile.first_name} {profile.last_name}

## Contact Information
- Email: {profile.email}
{f"- Phone: {profile.phone}" if profile.phone else ""}
{f"- Location: {profile.city}, {profile.state}, {profile.country}" if profile.city else ""}
{f"- LinkedIn: {profile.linkedin_url}" if profile.linkedin_url else ""}
{f"- GitHub: {profile.github_url}" if profile.github_url else ""}
{f"- Website: {profile.personal_website}" if profile.personal_website else ""}

## Professional Summary
{profile.about_me or "Professional looking to contribute skills and experience to a new opportunity."}

## Education
{_format_education_for_cv(educations)}

## Work Experience
{_format_experience_for_cv(experiences)}

## Skills
- Technical skills relevant to {job_description.title}
- Communication and teamwork
- Problem-solving abilities
"""

    return GeneratedCV(
        format="md",
        cv_text=cv_text.strip(),
    )


def review_from_user_and_job(profile: Profile, educations: list[Education],
                             experiences: list[Experience],
                             job_description: JobDescriptionResponse) -> ReviewResponse:
    """
    Given the full information about a user, generate a proper review of
    how likely this person will get this job.
    The provided information is:
    - profile description as present in the db
    - list of all user education entries
    - list of all user experience entries
    - job_description
    """
    # Create a prompt to analyze the match between candidate and job
    prompt = f"""
    Analyze this candidate for a job match and provide a score from 0-100 and suggestions.
    
    Job Title: {job_description.title}
    Company: {job_description.company_name}
    Job Description: {job_description.description}
    
    Candidate Information:
    Name: {profile.first_name} {profile.last_name}
    About: {profile.about_me or "Not provided"}
    
    Education:
    {_format_education(educations)}
    
    Experience:
    {_format_experience(experiences)}
    
    Please provide:
    1. A match score between 0-100
    2. 3-5 specific, skills-related suggestions for how the candidate can improve their chances
    Format your response as follows:
    SCORE: [number]
    SUGGESTIONS:
    - [suggestion 1]
    - [suggestion 2]
    - [suggestion 3]
    """

    # Call the AI model
    response = request_model(prompt)

    if not response:
        # Fallback if API fails
        return ReviewResponse(
            matchScore=50,
            suggestions=[
                "Unable to generate personalized suggestions. Consider reviewing your skills against the job description."]
        )

    # Parse the response
    try:
        score_line = None
        suggestions = []

        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith("SCORE:"):
                score_text = line.replace("SCORE:", "").strip()
                try:
                    score = int(score_text)
                    score = max(0, min(100, score))  # Ensure score is between 0-100
                except ValueError:
                    score = 50  # Default if parsing fails
            elif line.startswith("-") and len(line) > 2:
                suggestion = line[1:].strip()
                if suggestion and not suggestion.isspace():
                    suggestions.append(suggestion)

        # If no suggestions were found, add a generic one
        if not suggestions:
            suggestions = [
                f"Review your skills against the requirements for {job_description.title}",
                f"Consider highlighting specific achievements relevant to {job_description.company_name}",
                "Update your profile with more detailed technical skills"
            ]

        return ReviewResponse(
            matchScore=score if 'score' in locals() else 50,
            suggestions=suggestions[:5]  # Limit to 5 suggestions
        )

    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        return ReviewResponse(
            matchScore=50,
            suggestions=[
                f"Highlight relevant skills for {job_description.title}",
                f"Consider additional training in areas mentioned in the job description",
                f"Tailor your experience to match {job_description.company_name}'s requirements"
            ]
        )


if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
