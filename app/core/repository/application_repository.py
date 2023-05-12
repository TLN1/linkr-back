from typing import Optional, Protocol

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
    ) -> Optional[Application]:
        pass

    def get_application(self, id: int) -> Optional[Application]:
        pass