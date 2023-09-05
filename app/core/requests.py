from dataclasses import dataclass, field

# TODO maybe implement builder pattern for building requests
from app.core.models import (
    Account,
    Education,
    Experience,
    ExperienceLevel,
    Industry,
    JobLocation,
    JobType,
    OrganizationSize,
    Skill,
    SwipeDirection,
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


@dataclass
class UpdateUserRequest:
    username: str
    education: list[Education] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)


@dataclass
class UpdatePreferencesRequest:
    industry: list[Industry] = field(default_factory=list)
    job_location: list[JobLocation] = field(default_factory=list)
    job_type: list[JobType] = field(default_factory=list)
    experience_level: list[ExperienceLevel] = field(default_factory=list)


@dataclass
class SwipeApplicationRequest:
    application_id: int
    direction: SwipeDirection


@dataclass
class SwipeUserRequest:
    application_id: int
    swiped_username: str
    direction: SwipeDirection
