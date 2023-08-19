from dataclasses import dataclass, field

from app.core.models import Application, Company, Industry, OrganizationSize
from app.core.repository.company import ICompanyRepository


@dataclass
class InMemoryCompanyRepository(ICompanyRepository):
    companies: list[Company] = field(default_factory=list)

    def get_company(self, company_id: int) -> Company | None:
        for company in self.companies:
            if company.id == company_id:
                return company
        return None

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Company | None:
        self.companies.append(
            Company(
                id=len(self.companies),
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
            )
        )
        return self.companies[-1]

    def update_company(
        self,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Company | None:
        for company in self.companies:
            if company.id == company_id:
                company.name = name
                company.website = website
                company.industry = industry
                company.organization_size = organization_size
                return company
        return None

    def delete_company(self, company_id: int) -> bool:
        company_to_delete = None
        for company in self.companies:
            if company.id == company_id:
                company_to_delete = company

        if company_to_delete is not None:
            self.companies.remove(company_to_delete)
            return True

        return False

    def link_application(self, company_id: int, application: Application) -> bool:
        for company in self.companies:
            if company.id == company_id:
                company.link_application(application)
                return True

        return False
