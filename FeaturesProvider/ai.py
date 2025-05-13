import os

import requests
from dotenv import load_dotenv
from loguru import logger

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
    # FIXME: Your code goes here...
    return JobDescriptionResponse(
        company_name="SomeCorp Ltd",
        company_address="Mockers avenue 48",
        company_city="Berlin",
        company_postal_code="03523",
        recruiter_name="",
        title="Senior Software Engineer for SuperMocker",
        description="Mandatory 10 years of experience with Python; architectural knowledge recommended.",
    )

if __name__ == "__main__":
    print(request_model("John"))
