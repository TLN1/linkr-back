from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Optional

from app.core.models import Company, Industry, OrganizationSize
from app.core.repository.company_repository import ICompanyRepository


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
        image: bytes,
        image_type: str,
        cover_image: bytes,
        cover_image_type: str,
    ) -> Company | None:
        self.companies.append(
            Company(
                id=len(self.companies),
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image=image,
                image_type=image_type,
                cover_image=cover_image,
                cover_image_type=cover_image_type,
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
        image: bytes,
        image_type: str,
        cover_image: bytes,
        cover_image_type: str,
    ) -> Optional[Company]:
        for company in self.companies:
            if company.id == company_id:
                company.name = name
                company.website = website
                company.industry = industry
                company.organization_size = organization_size
                company.image = image
                company.image_type = image_type
                company.cover_image = cover_image
                company.cover_image_type = cover_image_type
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
            image,
            image_type,
            cover_image,
            cover_image_type,
        ) in cursor.execute("SELECT * FROM company WHERE id = ?", (company_id,)):
            return Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image=image,
                image_type=image_type,
                cover_image=cover_image,
                cover_image_type=cover_image_type,
            )
        return None

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
        company = None
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO company (company_name, website, industry, organization_size, "
            "image, image_type, cover_image, cover_image_type) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                name,
                website,
                str(industry),
                str(organization_size),
                image,
                image_type,
                cover_image,
                cover_image_type,
            ),
        )

        for (
            c_id,
            name,
            website,
            industry,
            organization_size,
            image,
            image_type,
            cover_image,
            cover_image_type,
        ) in cursor.execute("SELECT * FROM " "company ORDER BY " "id DESC " "LIMIT 1;"):
            company = Company(
                id=c_id,
                name=name,
                website=website,
                industry=industry,
                organization_size=organization_size,
                image=image,
                image_type=image_type,
                cover_image=cover_image,
                cover_image_type=cover_image_type,
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
        image: bytes,
        image_type: str,
        cover_image: bytes,
        cover_image_type: str,
    ) -> Optional[Company]:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE company company_name = ?, website = ?, industry = ?, "
            "organization_size = ?, image = ?, "
            "image_type = ?, cover_image = ?, cover_image_type = ? "
            "WHERE id = ?",
            (
                name,
                website,
                industry,
                organization_size,
                image,
                image_type,
                cover_image,
                cover_image_type,
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
