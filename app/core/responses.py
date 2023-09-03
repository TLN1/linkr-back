from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from app.core.constants import Status
from app.core.models import Application, User


class TokenResponse(BaseModel):
    token: str


@dataclass
class ApplicationsResponse(BaseModel):
    applications: list[Application]


class SwipeListResponse(BaseModel):
    swipe_list: list[Application] | list[User] = Field(default_factory=list)


@dataclass
class CoreResponse:
    status: Status = Status.OK
    response_content: BaseModel = field(default_factory=BaseModel)
