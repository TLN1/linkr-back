from typing import Protocol

from app.core.models import Application, Company, Industry, OrganizationSize


class ICompanyRepository(Protocol):
    def get_company(self, company_id: int) -> Company | None:
        pass

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Company | None:
        pass

    def update_company(
        self,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Company | None:
        pass

    def delete_company(self, company_id: int) -> bool:
        pass

    def link_application(self, company_id: int, application: Application) -> bool:
        pass
