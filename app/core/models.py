from enum import Enum

from pydantic import BaseModel, Field


# TODO: ADD VALUES
class Industry(Enum):
    SOFTWARE_ENGINEERING = "Software Engineering"

    def __str__(self) -> str:
        return self.value


# TODO: ADD VALUES
class OrganizationSize(Enum):
    SMALL = "1-10 employees"

    def __str__(self) -> str:
        return self.value


class JobLocation(Enum):
    ON_SITE = "on-site"
    REMOTE = "remote"


class JobType(Enum):
    PART_TIME = "part-time"
    FULL_TIME = "full-time"


class ExperienceLevel(Enum):
    INTERN = "intern"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class Benefit(BaseModel):
    pass


class Company(BaseModel):
    id: int
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize
    image: bytes
    image_type: str
    cover_image: bytes
    cover_image_type: str


class Preference(BaseModel):
    industry: list[Industry] = Field(default_factory=list)
    job_location: list[JobLocation] = Field(default_factory=list)
    job_type: list[JobType] = Field(default_factory=list)
    experience_level: list[ExperienceLevel] = Field(default_factory=list)


class Experience(BaseModel):
    name: str
    description: str


class Education(BaseModel):
    name: str
    description: str


class Skill(BaseModel):
    name: str
    description: str


class User(BaseModel):
    username: str
    education: list[Education] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    preference: Preference = Preference()

    def update(
        self,
        education: list[Education],
        skills: list[Skill],
        experience: list[Experience],
        preference: Preference,
    ) -> None:
        self.education = education
        self.skills = skills
        self.experience = experience
        self.preference = preference


class Account(BaseModel):
    id: int
    username: str
    password: str
    companies: list[int] = Field(default_factory=list)

    def link_company(self, company: Company) -> None:
        self.companies.append(company.id)


class Requirement(BaseModel):
    pass


class Application(BaseModel):
    id: int
    location: JobLocation
    job_type: JobType
    experience_level: ExperienceLevel
    requirements: list[Requirement]
    benefits: list[Benefit]
    views: int = 0

    def update(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> None:
        self.location = location
        self.job_type = job_type
        self.experience_level = experience_level
        self.requirements = requirements
        self.benefits = benefits


class ApplicationId(BaseModel):
    application_id: int


class InMemoryToken(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
