from database.db_interface import Education, Experience, Profile
from loguru import logger
from models import JobDescriptionResponse

from .ai_api import request_model


def analyze_gaps(
    profile: Profile,
    educations: list[Education],
    experiences: list[Experience],
    job_description: JobDescriptionResponse,
) -> dict:
    """
    Analyzes gaps between the candidate's profile and job requirements.
    Returns gaps categorized by severity: Critical, Important, Nice-to-have.

    The provided information is:
    - profile description as present in the db
    - list of all user education entries
    - list of all user experience entries
    - job_description (parsed)
    """
    # Create a prompt to identify experience gaps
    prompt = f"""
    Analyze this candidate's profile against the job requirements and identify experience or responsibility gaps.

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

    Identify SMALL experience or responsibility gaps where the candidate is missing information.
    Focus on borderline opportunities - gaps that could be filled with more details in their profile.

    Categorize each gap by severity:
    - CRITICAL: Must-have requirements that are completely missing (deal-breakers)
    - IMPORTANT: Strong requirements with weak or missing evidence
    - NICE-TO-HAVE: Additional improvements for a stronger candidacy

    For each gap, provide:
    1. What is missing or weak
    2. Specific suggestion on where/how to add more information

    Provide 3-7 total gaps across all severity levels.

    Format your response EXACTLY as follows:
    CRITICAL:
    - [gap description] | [specific suggestion]

    IMPORTANT:
    - [gap description] | [specific suggestion]
    - [gap description] | [specific suggestion]

    NICE-TO-HAVE:
    - [gap description] | [specific suggestion]
    """

    logger.info(f"Gap analysis prompt: {prompt}")

    # Call the AI model
    response = request_model(prompt)

    if not response:
        # Fallback if API fails
        return {
            "gaps": [
                {
                    "gap_text": "Unable to analyze gaps at this time",
                    "severity": "Important",
                    "suggestion": "Please try again later or manually review your profile against the job description."
                }
            ]
        }

    logger.info(f"Gap analysis received response: {response}")

    # Parse the response
    try:
        gaps = []
        current_severity = None

        lines = response.strip().split("\n")
        for line in lines:
            line = line.strip()

            # Check for severity headers
            if line.startswith("CRITICAL:"):
                current_severity = "Critical"
                continue
            elif line.startswith("IMPORTANT:"):
                current_severity = "Important"
                continue
            elif line.startswith("NICE-TO-HAVE:"):
                current_severity = "Nice-to-have"
                continue

            # Parse gap lines (format: "- gap text | suggestion")
            if line.startswith("-") and current_severity and "|" in line:
                line_content = line[1:].strip()  # Remove the "-" prefix
                parts = line_content.split("|", 1)

                if len(parts) == 2:
                    gap_text = parts[0].strip()
                    suggestion = parts[1].strip()

                    if gap_text and suggestion:
                        gaps.append({
                            "gap_text": gap_text,
                            "severity": current_severity,
                            "suggestion": suggestion
                        })

        # If no gaps were parsed, provide fallback gaps
        if not gaps:
            gaps = [
                {
                    "gap_text": f"Review alignment with {job_description.title} requirements",
                    "severity": "Important",
                    "suggestion": "Compare your experience descriptions against the key requirements listed in the job posting."
                },
                {
                    "gap_text": f"Highlight relevant achievements for {job_description.company_name}",
                    "severity": "Important",
                    "suggestion": "Add specific metrics and outcomes to your experience entries that relate to the job requirements."
                },
                {
                    "gap_text": "Expand technical skills section",
                    "severity": "Nice-to-have",
                    "suggestion": "Include more details about specific tools, technologies, or methodologies mentioned in the job description."
                }
            ]

        return {"gaps": gaps}

    except Exception as e:
        logger.error(f"Error parsing AI gap analysis response: {e}")
        return {
            "gaps": [
                {
                    "gap_text": "Error analyzing gaps",
                    "severity": "Important",
                    "suggestion": "Please review the job description manually and ensure your profile highlights relevant experience."
                }
            ]
        }


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
