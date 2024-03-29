from dataclasses import dataclass, field
from sqlite3 import Connection

from app.core.models import Application, Company, Industry, OrganizationSize
from app.core.repository.application import IApplicationRepository
from app.core.repository.company import ICompanyRepository


@dataclass
class InMemoryCompanyRepository(ICompanyRepository):
    application_repository: IApplicationRepository
    companies: list[Company] = field(default_factory=list)

    def get_company(self, company_id: int) -> Company | None:
        for company in self.companies:
            if company.id == company_id:
                company.applications = (
                    self.application_repository.get_company_applications(
                        company_id=company_id
                    )
                )
                return company

        return None

    def get_user_companies(self, username: str) -> list[Company]:
        result = []

        for company in self.companies:
            if company.owner_username == username:
                company.applications = (
                    self.application_repository.get_company_applications(
                        company_id=company.id
                    )
                )
                result.append(company)

        return result

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
        owner_username: str,
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
                owner_username=owner_username,
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
    application_repository: IApplicationRepository
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
            owner_username,
        ) in cursor.execute("SELECT * FROM company WHERE id = ?", (company_id,)):
            company = Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                cover_image_uri=cover_image_uri,
                owner_username=owner_username,
            )

            company.applications = self.application_repository.get_company_applications(
                company_id=c_id
            )
            return company

        return None

    def get_user_companies(self, username: str) -> list[Company]:
        result = []
        cursor = self.connection.cursor()
        for (
            c_id,
            name,
            website,
            industry,
            organization_size,
            image_uri,
            cover_image_uri,
            owner_username,
        ) in cursor.execute(
            "SELECT * FROM company WHERE owner_username = ?", (username,)
        ):
            company = Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                cover_image_uri=cover_image_uri,
                owner_username=owner_username,
            )

            company.applications = self.application_repository.get_company_applications(
                company_id=company.id
            )
            result.append(company)

        return result

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
        owner_username: str,
    ) -> Company | None:
        company = None
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO company (company_name, website, industry, organization_size, "
            "image_uri, cover_image_uri, owner_username) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                name,
                website,
                str(industry),
                str(organization_size),
                image_uri,
                cover_image_uri,
                owner_username,
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
            owner_username,
        ) in cursor.execute("SELECT * FROM company ORDER BY id DESC LIMIT 1;"):
            company = Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image_uri=image_uri,
                owner_username=owner_username,
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
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM company WHERE id = ?", [company_id])
        self.connection.commit()
        cursor.close()
        return self.get_company(company_id) is None

    def link_application(self, company_id: int, application: Application) -> bool:
        # TODO: IMPLEMENT
        return False
