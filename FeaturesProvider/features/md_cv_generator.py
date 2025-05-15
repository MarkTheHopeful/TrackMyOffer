from database.db_interface import Education, Experience, Profile
from loguru import logger
from models import GeneratedCV, JobDescriptionResponse

from .ai_api import request_model
from .review_user_application import _format_education, _format_experience


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
    {_format_education(educations)}
    
    WORK EXPERIENCE:
    {_format_experience(experiences)}
    
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
{f"- Phone: {profile.phone}" if profile.phone is not None else ""}
{f"- Location: {profile.city}, {profile.state}, {profile.country}" if profile.city is not None else ""}
{f"- LinkedIn: {profile.linkedin_url}" if profile.linkedin_url is not None else ""}
{f"- GitHub: {profile.github_url}" if profile.github_url is not None else ""}
{f"- Website: {profile.personal_website}" if profile.personal_website is not None else ""}

## Professional Summary
{profile.about_me or "Professional looking to contribute skills and experience to a new opportunity."}

## Education
{_format_education(educations)}

## Work Experience
{_format_experience(experiences)}

## Skills
- Technical skills relevant to {job_description.title}
- Communication and teamwork
- Problem-solving abilities
"""

    return GeneratedCV(
        format="md",
        cv_text=cv_text.strip(),
    )
