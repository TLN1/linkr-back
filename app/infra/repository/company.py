from dataclasses import dataclass, field
from sqlite3 import Connection

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
        image_uri: str,
        cover_image_uri: str,
    ) -> Company | None:
        self.companies.append(
            Company(
                id=len(self.companies),
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                cover_image_uri=cover_image_uri,
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
        image_uri: str,
        cover_image_uri: str,
    ) -> Company | None:
        for company in self.companies:
            if company.id == company_id:
                company.name = name
                company.website = website
                company.industry = industry
                company.organization_size = organization_size
                company.image_uri = image_uri
                company.cover_image_uri = cover_image_uri
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


@dataclass
class SqliteCompanyRepository(ICompanyRepository):
    connection: Connection

    def get_company(self, company_id: int) -> Company | None:
        cursor = self.connection.cursor()
        for (
            c_id,
            name,
            website,
            industry,
            organization_size,
            image_uri,
            cover_image_uri,
        ) in cursor.execute("SELECT * FROM company WHERE id = ?", (company_id,)):
            return Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                cover_image_uri=cover_image_uri,
            )
        return None

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
    ) -> Company | None:
        company = None
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO company (company_name, website, industry, organization_size, "
            "image_uri, cover_image_uri) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                name,
                website,
                str(industry),
                str(organization_size),
                image_uri,
                cover_image_uri,
            ),
        )

        for (
            c_id,
            name,
            website,
            industry,
            organization_size,
            image_uri,
            cover_image_uri,
        ) in cursor.execute("SELECT * FROM company ORDER BY id DESC LIMIT 1;"):
            company = Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                cover_image_uri=cover_image_uri,
            )
        self.connection.commit()
        cursor.close()
        return company

    def update_company(
        self,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
    ) -> Company | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE company SET company_name = ?, website = ?, industry = ?, "
            "organization_size = ?, "
            "image_uri = ?, cover_image_uri = ? "
            "WHERE id = ?",
            (
                name,
                website,
                str(industry),
                str(organization_size),
                image_uri,
                cover_image_uri,
                company_id,
            ),
        )

        self.connection.commit()
        cursor.close()
        return self.get_company(company_id)

    def delete_company(self, company_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM company WHERE id = ?", [company_id])
        return self.get_company(company_id) is None

    def link_application(self, company_id: int, application: Application) -> bool:
        # TODO: IMPLEMENT
        return False
