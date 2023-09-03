from dataclasses import dataclass, field

from pydantic import BaseModel

from app.core.constants import Status
from app.core.models import Application


class TokenResponse(BaseModel):
    token: str


@dataclass
class ApplicationsResponse(BaseModel):
    applications: list[Application]


@dataclass
class CoreResponse:
    status: Status = Status.OK
    response_content: BaseModel = field(default_factory=BaseModel)
