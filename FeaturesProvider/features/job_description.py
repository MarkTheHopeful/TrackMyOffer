from models import JobDescriptionResponse


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
