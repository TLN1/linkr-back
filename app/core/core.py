from dataclasses import dataclass

from pydantic import BaseModel

from app.core.constants import Status
from app.core.models import (
    Account,
    ApplicationId,
    Industry,
    OrganizationSize,
    Preference,
    SwipeDirection,
)
from app.core.requests import (
    ApplicationInteractionRequest,
    CreateApplicationRequest,
    DeleteApplicationRequest,
    GetApplicationRequest,
    RegisterRequest,
    SetupUserRequest,
    UpdateApplicationRequest,
    UpdatePreferencesRequest,
)
from app.core.responses import ApplicationsResponse, CoreResponse, SwipeListResponse
from app.core.services.account import AccountService
from app.core.services.application import ApplicationService
from app.core.services.company import CompanyService
from app.core.services.match import MatchService
from app.core.services.user import UserService


@dataclass
class Core:
    account_service: AccountService
    company_service: CompanyService
    application_service: ApplicationService
    user_service: UserService
    match_service: MatchService

    def register(self, request: RegisterRequest) -> CoreResponse:
        status, account = self.account_service.register(
            username=request.username, password=request.password
        )

        if status != Status.OK or account is None:
            return CoreResponse(status=status)

        status, user = self.user_service.create_user(account)

        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(
            status=status, response_content=account  # login_response.response_content
        )

    def get_user(self, username: str) -> CoreResponse:
        status, user = self.user_service.get_user(username=username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=user)

    def update_user(self, request: SetupUserRequest) -> CoreResponse:
        status, user = self.user_service.update_user(
            account=request.account, user=request.user
        )
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=user)

    def update_preferences(
        self, account: Account, request: UpdatePreferencesRequest
    ) -> CoreResponse:
        status, user = self.user_service.update_preferences(
            account=account,
            preference=Preference(
                industry=request.industry,
                job_type=request.job_type,
                job_location=request.job_location,
                experience_level=request.experience_level,
            ),
        )

        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=user)

    def create_application(
        self, account: Account, request: CreateApplicationRequest
    ) -> CoreResponse:
        company = self.company_service.get_company(request.company_id)
        if company is None or company.owner_username != account.username:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        status, application = self.application_service.create_application(
            title=request.title,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            skills=request.skills,
            description=request.description,
            company_id=request.company_id,
        )

        if status != Status.OK or application is None:
            return CoreResponse(status)

        return CoreResponse(
            status=status, response_content=ApplicationId(application_id=application.id)
        )

    def get_application(self, request: GetApplicationRequest) -> CoreResponse:
        status, application = self.application_service.get_application(id=request.id)

        application_response = BaseModel() if application is None else application
        return CoreResponse(status=status, response_content=application_response)

    def get_applications(self, company_id: int) -> CoreResponse:
        company = self.company_service.get_company(company_id)
        if company is None:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        applications = self.application_service.get_applications(company_id)

        return CoreResponse(
            status=Status.OK,
            response_content=ApplicationsResponse(applications=applications),
        )

    def update_application(
        self, account: Account, request: UpdateApplicationRequest
    ) -> CoreResponse:
        status, application = self.application_service.get_application(request.id)
        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        company = self.company_service.get_company(application.company_id)
        if company is None or company.owner_username != account.username:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        status, application = self.application_service.update_application(
            id=request.id,
            title=request.title,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            skills=request.skills,
            description=request.description,
        )

        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=application)

    def application_interaction(
        self, request: ApplicationInteractionRequest
    ) -> CoreResponse:
        status = self.application_service.application_interaction(id=request.id)
        return CoreResponse(status=status)

    def delete_application(self, request: DeleteApplicationRequest) -> CoreResponse:
        status = self.application_service.delete_application(id=request.id)
        return CoreResponse(status=status)

    def create_company(
        self,
        account: Account,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
        image_uri: str,
        cover_image_uri: str,
    ) -> CoreResponse:
        status, company = self.company_service.create_company(
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image_uri=image_uri,
            cover_image_uri=cover_image_uri,
            owner_username=account.username,
        )

        if company is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=company)

    def get_company(self, company_id: int) -> CoreResponse:
        company = self.company_service.get_company(company_id=company_id)
        if company is None:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        return CoreResponse(status=Status.OK, response_content=company)

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
    ) -> CoreResponse:
        status, company = self.company_service.update_company(
            account=account,
            company_id=company_id,
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
            image_uri=image_uri,
            cover_image_uri=cover_image_uri,
        )
        if company is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=company)

    def delete_company(self, account: Account, company_id: int) -> CoreResponse:
        status = self.company_service.delete_company(
            account=account, company_id=company_id
        )
        return CoreResponse(status=status)

    def get_swipe_list_users(
        self, swiper_application_id: int, amount: int
    ) -> CoreResponse:
        status, application = self.application_service.get_application(
            id=swiper_application_id
        )
        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        status, swipe_list = self.match_service.get_swipe_list_users(
            swiper_application_id=swiper_application_id, amount=amount
        )

        if status != Status.OK:
            return CoreResponse(status=status)

        return CoreResponse(
            status=status, response_content=SwipeListResponse(swipe_list=swipe_list)
        )

    def get_swipe_list_applications(
        self, account: Account, amount: int
    ) -> CoreResponse:
        status, user = self.user_service.get_user(username=account.username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        status, swipe_list = self.match_service.get_swipe_list_applications(
            swiper_username=user.username, preference=user.preference, amount=amount
        )

        if status != Status.OK:
            return CoreResponse(status=status)

        return CoreResponse(
            status=status, response_content=SwipeListResponse(swipe_list=swipe_list)
        )

    def _match(self, username: str, application_id: int) -> None:
        status, application = self.application_service.get_application(
            id=application_id
        )
        if status != Status.OK or application is None:
            return

        company = self.company_service.get_company(company_id=application.company_id)
        if company is None:
            return

        status, user = self.user_service.get_user(username=company.owner_username)
        if status != Status.OK or user is None:
            return

        if username != user.username:
            # TODO: open chat
            print(f"Chat between user: {username} and user: {user.username}")

    def swipe_application(
        self, swiper_username: str, application_id: int, direction: SwipeDirection
    ) -> CoreResponse:
        status, application = self.application_service.get_application(
            id=application_id
        )
        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        status, user = self.user_service.get_user(username=swiper_username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        status, matched = self.match_service.swipe_application(
            swiper_username=swiper_username,
            application_id=application_id,
            direction=direction,
        )

        if matched:
            self._match(username=swiper_username, application_id=application_id)

        return CoreResponse(status=status)

    def swipe_user(
        self,
        swiper_application_id: int,
        swiped_username: str,
        direction: SwipeDirection,
    ) -> CoreResponse:
        status, user = self.user_service.get_user(username=swiped_username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        status, application = self.application_service.get_application(
            id=swiper_application_id
        )
        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        status, matched = self.match_service.swipe_user(
            swiper_application_id=swiper_application_id,
            swiped_username=swiped_username,
            direction=direction,
        )

        if matched:
            self._match(username=swiped_username, application_id=swiper_application_id)

        return CoreResponse(status=status)
