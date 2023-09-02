from dataclasses import dataclass

# TODO maybe implement builder pattern for building requests
from app.core.models import (
    Account,
    ExperienceLevel,
    Industry,
    JobLocation,
    JobType,
    OrganizationSize,
    User,
)


@dataclass
class RegisterRequest:
    username: str
    password: str


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class AccountRequest:
    # token: str
    account: Account


@dataclass
class GetUserRequest:
    username: str


@dataclass
class SetupUserRequest(AccountRequest):
    user: User


@dataclass
class LogoutRequest(AccountRequest):
    pass


@dataclass
class CreateApplicationRequest(AccountRequest):
    location: JobLocation = JobLocation.ON_SITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.JUNIOR
    description: str = ""
    company_id: int = 0


@dataclass
class UpdateApplicationRequest(AccountRequest):
    id: int
    location: JobLocation = JobLocation.ON_SITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.JUNIOR
    description: str = ""


@dataclass
class GetApplicationRequest(AccountRequest):
    id: int


@dataclass
class ApplicationInteractionRequest(AccountRequest):
    id: int


@dataclass
class DeleteApplicationRequest(AccountRequest):
    id: int


# FIXME
@dataclass
class CreateCompanyRequest:
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize
    image_uri: str
    cover_image_uri: str
