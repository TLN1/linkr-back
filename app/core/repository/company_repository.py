from typing import Optional, Protocol

from app.core.models import Company, Industry, OrganizationSize


class ICompanyRepository(Protocol):
    def get_company(self, company_id: int) -> Company | None:
        pass

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image: bytes,
        image_type: str,
        cover_image: bytes,
        cover_image_type: str,
    ) -> Company | None:
        pass

    def update_company(
        self,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image: bytes,
        image_type: str,
        cover_image: bytes,
        cover_image_type: str,
    ) -> Optional[Company]:
        pass

    def delete_company(self, company_id: int) -> bool:
        pass
