from typing import Protocol

from app.core.models import (
    Application,
    Benefit,
    ExperienceLevel,
    JobLocation,
    JobType,
    Requirement,
)


class IApplicationRepository(Protocol):
    def create_application(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> Application | None:
        pass

    def get_application(self, id: int) -> Application | None:
        pass

    def has_application(self, id: int) -> bool:
        pass

    def update_application(
        self,
        id: int,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> Application | None:
        pass

    def application_interaction(self, id: int) -> bool:
        pass

    def delete_application(self, id: int) -> bool:
        pass
