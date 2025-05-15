from database.db_interface import Education, Experience, Profile
from models import JobDescriptionResponse, ReviewResponse


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
