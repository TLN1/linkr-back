from typing import Protocol

from app.core.models import (
    Application,
    ExperienceLevel,
    JobLocation,
    JobType,
    Preference,
)


class IApplicationRepository(Protocol):
    def create_application(
        self,
        title: str,
        experience_level: ExperienceLevel,
        location: JobLocation,
        job_type: JobType,
        skills: list[str],
        description: str,
        company_id: int
    ) -> Application | None:
        pass

    def get_application(self, id: int) -> Application | None:
        pass

    def get_swipe_applications(
        self, limit: int, preference: Preference
    ) -> list[Application]:
        pass

    def get_company_applications(self, company_id: int) -> list[Application]:
        pass

    def has_application(self, id: int) -> bool:
        pass

    def update_application(
        self,
        id: int,
        title: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        skills: list[str],
        description: str,
    ) -> Application | None:
        pass

    def application_interaction(self, id: int) -> bool:
        pass

    def delete_application(self, id: int) -> bool:
        pass
