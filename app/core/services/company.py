from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Account, Application, Company, Industry, OrganizationSize
from app.core.repository.company import ICompanyRepository


@dataclass
class CompanyService:
    company_repository: ICompanyRepository

    def get_company(self, company_id: int) -> Company | None:
        return self.company_repository.get_company(company_id=company_id)

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
    ) -> tuple[Status, Company | None]:
        company = self.company_repository.create_company(
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image_uri=image_uri,
            cover_image_uri=cover_image_uri,
        )
        if company is None:
            return Status.ERROR_CREATING_COMPANY, company

        return Status.OK, company

    def update_company(
        self,
        account: Account,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
    ) -> tuple[Status, Company | None]:
        if company_id not in account.companies:
            return Status.COMPANY_DOES_NOT_EXIST, None

        company = self.company_repository.update_company(
            company_id=company_id,
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image_uri=image_uri,
            cover_image_uri=cover_image_uri,
        )
        if company is None:
            return Status.COMPANY_DOES_NOT_EXIST, None

        return Status.OK, company

    def delete_company(self, account: Account, company_id: int) -> Status:
        if company_id not in account.companies:
            return Status.COMPANY_DOES_NOT_EXIST

        if self.company_repository.delete_company(company_id=company_id):
            return Status.OK
        return Status.ERROR_DELETING_COMPANY

    def link_application(self, company_id: int, application: Application) -> Status:
        if not self.company_repository.link_application(
            company_id=company_id, application=application
        ):
            return Status.APPLICATION_CREATE_ERROR

        return Status.OK
