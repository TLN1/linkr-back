import base64
from dataclasses import dataclass
from typing import Optional

from fastapi import UploadFile

from app.core.constants import Status
from app.core.models import Account, Company, Industry, OrganizationSize
from app.core.repository.company_repository import ICompanyRepository


@dataclass
class CompanyService:
    company_repository: ICompanyRepository

    def get_company(self, company_id: int) -> Optional[Company]:
        return self.company_repository.get_company(company_id=company_id)

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image: UploadFile,
        cover_image: UploadFile,
    ) -> tuple[Status, Optional[Company]]:
        if image.content_type not in ["image/jpeg", "image/png"]:
            return Status.UNSUPPORTED_IMAGE_FORMAT, None

        if cover_image.content_type not in ["image/jpeg", "image/png"]:
            return Status.UNSUPPORTED_IMAGE_FORMAT, None

        image_bytes = base64.b64encode(image.file.read())
        cover_image_bytes = base64.b64encode(cover_image.file.read())

        company = self.company_repository.create_company(
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image=image_bytes,
            image_type=image.content_type,
            cover_image=cover_image_bytes,
            cover_image_type=cover_image.content_type,
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
        image: UploadFile,
        cover_image: UploadFile,
    ) -> tuple[Status, Optional[Company]]:
        if company_id not in account.companies:
            return Status.COMPANY_DOES_NOT_EXIST, None

        if image.content_type not in ["image/jpeg", "image/png"]:
            return Status.UNSUPPORTED_IMAGE_FORMAT, None

        if cover_image.content_type not in ["image/jpeg", "image/png"]:
            return Status.UNSUPPORTED_IMAGE_FORMAT, None

        image_bytes = base64.b64encode(image.file.read())
        cover_image_bytes = base64.b64encode(cover_image.file.read())

        company = self.company_repository.update_company(
            company_id=company_id,
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image=image_bytes,
            image_type=image.content_type,
            cover_image=cover_image_bytes,
            cover_image_type=cover_image.content_type,
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
