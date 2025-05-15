from models import JobDescriptionResponse
from .ai_api import request_model


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
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")

        parsed = json.loads(json_match.group())

        # Validate required fields
        required_fields = [
            "company_name",
            "company_address",
            "company_city",
            "company_postal_code",
            "recruiter_name",
            "title",
            "description",
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
