from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Application, ExperienceLevel, JobLocation, JobType
from app.core.repository.application import IApplicationRepository


# TODO: application is posted by logged in account for update, delete
@dataclass
class ApplicationService:
    application_repository: IApplicationRepository

    def create_application(
        self,
        title: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        skills: list[str],
        description: str,
        company_id: int,
    ) -> tuple[Status, Application | None]:
        application = self.application_repository.create_application(
            title=title,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            skills=skills,
            description=description,
            company_id=company_id,
        )

        if application is None:
            return Status.APPLICATION_CREATE_ERROR, None

        return Status.OK, application

    def get_application(self, id: int) -> tuple[Status, Application | None]:
        application = self.application_repository.get_application(id=id)
        if application is None:
            return Status.APPLICATION_DOES_NOT_EXIST, None

        return Status.OK, application

    def update_application(
        self,
        id: int,
        title: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        skills: list[str],
        description: str,
    ) -> tuple[Status, Application | None]:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST, None

        application = self.application_repository.update_application(
            id=id,
            title=title,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            skills=skills,
            description=description,
        )

        if application is None:
            return Status.APPLICATION_UPDATE_ERROR, None

        return Status.OK, application

    def application_interaction(self, id: int) -> Status:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.application_interaction(id=id):
            return Status.APPLICATION_INTERACTION_ERROR

        return Status.OK

    def delete_application(self, id: int) -> Status:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.delete_application(id=id):
            return Status.APPLICATION_DELETE_ERROR

        return Status.OK

    def get_applications(self, company_id: int) -> list[Application]:
        return self.application_repository.get_company_applications(company_id)
