from typing import Protocol

from app.core.models import Application, Company, Industry, OrganizationSize


class ICompanyRepository(Protocol):
    def get_company(self, company_id: int) -> Company | None:
        pass

    def get_user_companies(self, username: str) -> list[Company]:
        pass

    def create_company(
            self,
            name: str,
            website: str,
            industry: Industry,
            organization_size: OrganizationSize,
            description: str,
            image_uri: str,
            cover_image_uri: str,
            owner_username: str,
    ) -> Company | None:
        pass

    def update_company(
            self,
            company_id: int,
            name: str,
            website: str,
            industry: Industry,
            organization_size: OrganizationSize,
            description: str,
            image_uri: str,
            cover_image_uri: str,
    ) -> Company | None:
        pass

    def delete_company(self, company_id: int) -> bool:
        pass

    def link_application(self, company_id: int, application: Application) -> bool:
        pass
