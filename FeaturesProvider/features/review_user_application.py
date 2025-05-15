from database.db_interface import Education, Experience, Profile
from loguru import logger
from models import JobDescriptionResponse, ReviewResponse

from .ai_api import request_model


def review_from_user_and_job(
    profile: Profile,
    educations: list[Education],
    experiences: list[Experience],
    job_description: JobDescriptionResponse,
) -> ReviewResponse:
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

    logger.info(f"Review user prompt: {prompt}")

    # Call the AI model
    response = request_model(prompt)

    if not response:
        # Fallback if API fails
        return ReviewResponse(
            matchScore=50,
            suggestions=[
                "Unable to generate personalized suggestions. Consider reviewing your skills against the job description."
            ],
        )

    logger.info(f"Review user received response: {response}")

    # Parse the response
    try:
        score_line = None
        suggestions = []

        lines = response.strip().split("\n")
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
                "Update your profile with more detailed technical skills",
            ]

        return ReviewResponse(
            matchScore=score if "score" in locals() else 50,
            suggestions=suggestions[:5],  # Limit to 5 suggestions
        )

    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        return ReviewResponse(
            matchScore=50,
            suggestions=[
                f"Highlight relevant skills for {job_description.title}",
                "Consider additional training in areas mentioned in the job description",
                f"Tailor your experience to match {job_description.company_name}'s requirements",
            ],
        )


def _format_education(educations: list[Education]) -> str:
    """Helper function to format education information for the prompt"""
    if not educations:
        return "No formal education provided"

    edu_text = []
    for edu in educations:
        end_date = edu.end_date.strftime("%Y-%m") if edu.end_date is not None else "Present"
        edu_text.append(
            f"- {edu.institution}, {edu.degree}, {edu.start_date.strftime('%Y-%m')} to {end_date}"
            + (f", {edu.additional_info}" if edu.additional_info is not None else "")
        )

    return "\n".join(edu_text)


def _format_experience(experiences: list[Experience]) -> str:
    """Helper function to format experience information for the prompt"""
    if not experiences:
        return "No work experience provided"

    exp_text = []
    for exp in experiences:
        end_date = exp.end_date if exp.end_date is not None else "Present"
        exp_text.append(
            f"- {exp.company}, {exp.job_title}, {exp.start_date} to {end_date}"
            + (f"\n  {exp.description}" if exp.description is not None else "")
        )

    return "\n".join(exp_text)
