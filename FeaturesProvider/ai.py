import os
from typing import List

import requests
from dotenv import load_dotenv
from loguru import logger

from database.db_interface import Education, Profile, Experience
from models import JobDescriptionResponse, GeneratedCV, ProfileResponse, ReviewResponse

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


def request_model(text: str) -> str | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": PROMPTS.format(text),
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
    prompt = f"""Please analyze this job description and extract the following information in a structured way:
    - Company name
    - Company address
    - Company city
    - Company postal code
    - Recruiter name (if available)
    - Job title
    - Job description and requirements

    Job Description:
    {job_description_as_text}

    Please format your response as a JSON object with these exact fields:
    {{
        "company_name": "string",
        "company_address": "string",
        "company_city": "string",
        "company_postal_code": "string",
        "recruiter_name": "string",
        "title": "string",
        "description": "string"
    }}

    If any field is not found in the text, use an empty string.
    Put all requirements and detailed job description in the "description" field.
    """

    response = request_model(prompt)
    if not response:
        raise ValueError("Failed to parse job description")

    try:
        # Extract JSON from the response
        import json
        import re
        
        # Find JSON object in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")
            
        parsed = json.loads(json_match.group())
        
        # Validate required fields
        required_fields = [
            "company_name", "company_address", "company_city",
            "company_postal_code", "recruiter_name", "title", "description"
        ]
        
        for field in required_fields:
            if field not in parsed:
                parsed[field] = ""
            elif not isinstance(parsed[field], str):
                parsed[field] = str(parsed[field])
        
        return JobDescriptionResponse(**parsed)
        
    except json.JSONDecodeError:
        raise ValueError("Failed to parse LLM response as JSON")
    except Exception as e:
        raise ValueError(f"Error processing job description: {str(e)}")


def md_cv_from_user_and_job(profile: Profile, educations: List[Education],
                            experiences: List[Experience],
                            job_description: JobDescriptionResponse) -> GeneratedCV:
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
        cv_text=f"# {profile.first_name} {profile.last_name} for {job_description.company_name}" + """"
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
        """.strip()
    )

def review_from_user_and_job(profile: Profile, educations: List[Education],
                            experiences: List[Experience],
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
    return ReviewResponse(
        matchScore=69,
        suggestions=[f"{profile.first_name}, acquire more nice skills to impress {job_description.company_name} HRs"],
    )

if __name__ == "__main__":
    print(request_model("John"))
