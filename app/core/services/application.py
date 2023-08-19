from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import (
    Account,
    Application,
    Benefit,
    ExperienceLevel,
    JobLocation,
    JobType,
    Requirement,
)
from app.core.repository.application import IApplicationRepository


# TODO: application is posted by logged in account for update, delete
@dataclass
class ApplicationService:
    application_repository: IApplicationRepository

    def create_application(
        self,
        account: Account,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> tuple[Status, Application | None]:
        application = self.application_repository.create_application(
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
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
        account: Account,
        id: int,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> tuple[Status, Application | None]:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST, None

        application = self.application_repository.update_application(
            id=id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        )

        if application is None:
            return Status.APPLICATION_UPDATE_ERROR, None

        return Status.OK, application

    def application_interaction(self, account: Account, id: int) -> Status:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.application_interaction(id=id):
            return Status.APPLICATION_INTERACTION_ERROR

        return Status.OK

    def delete_application(self, account: Account, id: int) -> Status:
        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.delete_application(id=id):
            return Status.APPLICATION_DELETE_ERROR

        return Status.OK
