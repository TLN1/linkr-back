from dataclasses import dataclass, field

from app.core.models import Application, ExperienceLevel, JobLocation, JobType
from app.core.repository.application import IApplicationRepository


@dataclass
class InMemoryApplicationRepository(IApplicationRepository):
    applications: dict[int, Application] = field(default_factory=dict)
    _application_id: int = 0

    def _next_id(self) -> int:
        self._application_id += 1
        return self._application_id

    def create_application(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        description: str,
    ) -> Application | None:
        application_id = self._next_id()
        application = Application(
            id=application_id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            description=description,
            views=0,
        )

        self.applications[application_id] = application
        return application

    def get_application(self, id: int) -> Application | None:
        return self.applications.get(id)

    def has_application(self, id: int) -> bool:
        return self.get_application(id=id) is not None

    def update_application(
        self,
        id: int,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        description: str,
    ) -> Application | None:
        if not self.has_application(id=id):
            return None

        self.applications[id].update(
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            description=description,
        )

        return self.applications[id]

    def application_interaction(self, id: int) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications[id].views += 1
        return True

    def delete_application(self, id: int) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications.pop(id)
        return True
