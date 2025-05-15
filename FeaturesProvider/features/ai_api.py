import os

import requests
from database.db_interface import Education, Experience, Profile
from dotenv import load_dotenv
from loguru import logger
from models import GeneratedCV, JobDescriptionResponse

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
    # FIXME: Your code goes here...
    return GeneratedCV(
        format="md",
        cv_text=f"# {profile.first_name} {profile.last_name} for {job_description.company_name}"
        + """"
Physicist, Mathematician, Cambridge professor.

[isaac@applesdofall.org](isaac@applesdofall.org)

[http://en.wikipedia.org/wiki/Isaac_Newton](My website)

## Currently

Looking for a job as a computer scientist

### Specialized in

Laws of motion, gravitation, minting coins

### Research interests

Cooling, power series, optics, alchemy, planetary motions, apples.

## Education

`1654-1660`
__The King's School, Grantham.__

`June 1661 - now`
__Trinity College, Cambridge__

## Occupation

`1600`
__Royal Mint__, London

- Warden
- Minted coins

`1600`
__Lucasian professor of Mathematics__, Cambridge University
        """.strip(),
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
            suggestions=["Unable to generate personalized suggestions. Consider reviewing your skills against the job description."]
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


def _format_education(educations: list[Education]) -> str:
    """Helper function to format education information for the prompt"""
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


def _format_experience(experiences: list[Experience]) -> str:
    """Helper function to format experience information for the prompt"""
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



if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
