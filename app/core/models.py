from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

# TODO: maybe replace Enums with StrEnums?


class SwipeFor(StrEnum):
    USER = "user"
    APPLICATION = "application"


class SwipeDirection(StrEnum):
    LEFT = "left"
    RIGHT = "right"


# TODO: ADD VALUES
class Industry(StrEnum):
    SOFTWARE_ENGINEERING = "Software Engineering"

    def __str__(self) -> str:
        return self.value


# TODO: ADD VALUES
class OrganizationSize(StrEnum):
    SMALL = "1-10 employees"

    def __str__(self) -> str:
        return self.value


class JobLocation(StrEnum):
    ON_SITE = "On-site"
    REMOTE = "Remote"
    HYBRID = "Hybrid"

    def __str__(self) -> str:
        return self.value


class JobType(StrEnum):
    PART_TIME = "Part-time"
    FULL_TIME = "Full-time"

    def __str__(self) -> str:
        return self.value


class ExperienceLevel(StrEnum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"

    def __str__(self) -> str:
        return self.value


class Application(BaseModel):
    id: int
    title: str
    location: JobLocation
    job_type: JobType
    experience_level: ExperienceLevel
    skills: list[str]
    description: str
    company_id: int
    views: int = 0

    def update(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        description: str,
    ) -> None:
        self.location = location
        self.job_type = job_type
        self.experience_level = experience_level
        self.description = description


class Company(BaseModel):
    id: int
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize
    image_uri: str
    cover_image_uri: str
    owner_username: str
    applications: list[Application] = Field(default_factory=list)

    def link_application(self, application: Application) -> None:
        self.applications.append(application)


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
    preference: Preference = Field(default_factory=Preference)

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
    username: str
    password: str
    companies: list[Company] = Field(default_factory=list)

    def link_company(self, company: Company) -> None:
        self.companies.append(company)

    def has_company_with_id(self, company_id: int) -> bool:
        filtered = list(
            filter(lambda company: company.id == company_id, self.companies)
        )
        return len(filtered) > 0


class SwipeList(BaseModel):
    swipe_list: list[Application] | list[User] = Field(default_factory=list)


class ApplicationId(BaseModel):
    application_id: int


class InMemoryToken(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Message(BaseModel):
    sender_username: str
    recipient_username: str
    time: str
    text: str


class Chat(BaseModel):
    chat_id: int
    username1: str
    username2: str
    message_list: list[Message] = Field(default_factory=list)


class UserChats(BaseModel):
    chats: list[Chat] = Field(default_factory=list)
