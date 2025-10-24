from database.db_interface import Education, Experience, Profile
from loguru import logger
from models import GeneratedCV, JobDescriptionResponse

from .ai_api import request_model
from .prompt_templates import get_system_prompt
from .review_user_application import _format_education, _format_experience


def md_cv_from_user_and_job(
    profile: Profile,
    educations: list[Education],
    experiences: list[Experience],
    job_description: JobDescriptionResponse,
    region: str | None = None,
) -> GeneratedCV:
    """
    Given the full information about a user, generate a tailored markdown CV
    The provided information is:
    - profile description as present in the db
    - list of all user education entries
    - list of all user experience entries
    - job_description
    """

    system_prompt = get_system_prompt(region)

    # Create a comprehensive prompt for the AI model
    user_prompt = (
        "Use the candidate information below to produce a localized CV tailored to the target role. "
        "Structure the response as a complete document and focus on relevance to the job description.\n\n"
        "CANDIDATE INFORMATION:\n"
        f"Full Name: {profile.first_name} {profile.last_name}\n"
        f"Email: {profile.email}\n"
        f"Location: {profile.city or ''}, {profile.state or ''}, {profile.country or ''}\n"
        f"Phone: {profile.phone or 'Not provided'}\n"
        f"LinkedIn: {profile.linkedin_url or 'Not provided'}\n"
        f"GitHub: {profile.github_url or 'Not provided'}\n"
        f"Personal Website: {profile.personal_website or 'Not provided'}\n"
        f"Other URL: {profile.other_url or 'Not provided'}\n"
        f"About Me: {profile.about_me or 'Not provided'}\n\n"
        "EDUCATION:\n"
        f"{_format_education(educations)}\n\n"
        "WORK EXPERIENCE:\n"
        f"{_format_experience(experiences)}\n\n"
        "TARGET JOB:\n"
        f"Company: {job_description.company_name}\n"
        f"Position: {job_description.title}\n"
        f"Job Description: {job_description.description}\n\n"
        "Return only the completed document."
    )

    # Call the AI model
    cv_text = request_model(user_prompt, system_prompt=system_prompt)

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
