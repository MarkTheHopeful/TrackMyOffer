import os

import requests
from database.db_interface import Education, Experience, Profile
from dotenv import load_dotenv
from loguru import logger
from models import GeneratedCV, JobDescriptionResponse, ReviewResponse

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


def text_job_position_from_link(link_as_text: str) -> str:
    """
    Fetches given link to the job position and extracts text description of the position
    and the company which posted the position.
    If the link provided is unreachable or does not contain a job position, throw an error
    Otherwise provide job description as a text description.
    The job description should contain:
    - Company name, address, (city, postal code and a recruiter's name if possible)
    - Job title
    - Job description
    All in text form, possible to parse for human and an LLM
    """
    # FIXME: Your code goes here...
    return """
    SomeCorp Ltd, located on Mockers avenue 48, 03523 Berlin, looks for a Senior Software Engineer for their project SuperMocker. 
    
    Minimum 10 years of experience with Python is mandatory, architectural knowledge is highly recommended. 
    """.strip()


def job_description_from_text(job_description_as_text: str) -> JobDescriptionResponse:
    """
    Given the description of a position, possibly containing information about a company,
    and containing basic job description along with requirements,
    extract and parse the text into a JobDescriptionResponse object.
    Everything that does not fit into specific fields of the object should be concisely
    put into the `description` field (things like requirements or such).
    If the text does not appear to be a job description, throw an error
    """
    # FIXME: Your code goes here...
    return JobDescriptionResponse(
        company_name=job_description_as_text[:5],
        company_address="Mockers avenue 48",
        company_city="Berlin",
        company_postal_code="03523",
        recruiter_name="",
        title="Senior Software Engineer for SuperMocker",
        description="Mandatory 10 years of experience with Python; architectural knowledge recommended.",
    )


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
    return ReviewResponse(
        matchScore=69,
        suggestions=[f"{profile.first_name}, acquire more nice skills to impress {job_description.company_name} HRs"],
    )


if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
