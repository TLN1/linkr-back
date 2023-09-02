from dataclasses import dataclass, field

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
class CreateApplicationRequest:
    title: str
    company_id: int
    location: JobLocation
    job_type: JobType
    experience_level: ExperienceLevel
    description: str
    skills: list[str] = field(default_factory=list)


@dataclass
class UpdateApplicationRequest:
    id: int
    title: str
    location: JobLocation
    job_type: JobType
    experience_level: ExperienceLevel
    skills: list[str]
    description: str


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
