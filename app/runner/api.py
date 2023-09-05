from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.application_context import IApplicationContext
from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.models import (
    Account,
    Application,
    ApplicationId,
    Company,
    ExperienceLevel,
    Industry,
    OrganizationSize,
    Preference,
    SwipeDirection,
    Token,
    User, JobType, JobLocation,
)
from app.core.requests import (
    ApplicationInteractionRequest,
    CreateApplicationRequest,
    CreateCompanyRequest,
    DeleteApplicationRequest,
    GetApplicationRequest,
    RegisterRequest,
    SetupUserRequest,
    UpdateApplicationRequest,
    UpdatePreferencesRequest,
    UpdateUserRequest, SwipeApplicationRequest, SwipeUserRequest,
)
from app.core.responses import CoreResponse, SwipeListResponse
from app.core.services.account import AccountService
from app.core.services.application import ApplicationService
from app.core.services.company import CompanyService
from app.core.services.match import MatchService
from app.core.services.user import UserService
from app.infra.application_context import (
    InMemoryApplicationContext,
    InMemoryOauthApplicationContext,
)
from app.infra.auth_utils import oauth2_scheme, pwd_context
from app.infra.db_setup import ConnectionProvider
from app.infra.repository.account import SqliteAccountRepository
from app.infra.repository.application import SqliteApplicationRepository
from app.infra.repository.company import SqliteCompanyRepository
from app.infra.repository.match import SqliteMatchRepository
from app.infra.repository.user import SqliteUserRepository

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

match_repository = SqliteMatchRepository(connection=ConnectionProvider.get_connection())
user_repository = SqliteUserRepository(connection=ConnectionProvider.get_connection())
application_repository = SqliteApplicationRepository(
    connection=ConnectionProvider.get_connection()
)
company_repository = SqliteCompanyRepository(
    application_repository=application_repository,
    connection=ConnectionProvider.get_connection(),
)
account_repository = SqliteAccountRepository(
    company_repository=company_repository,
    connection=ConnectionProvider.get_connection(),
)

in_memory_application_context = InMemoryApplicationContext(
    account_repository=account_repository, hash_verifier=pwd_context.verify
)
in_memory_oauth_application_context = InMemoryOauthApplicationContext(
    account_repository=account_repository, hash_verifier=pwd_context.verify
)


def get_application_context() -> IApplicationContext:
    return in_memory_oauth_application_context


def get_core() -> Core:
    return Core(
        account_service=AccountService(
            account_repository=account_repository,
            hash_function=pwd_context.hash,
        ),
        application_service=ApplicationService(
            application_repository=application_repository,
        ),
        user_service=UserService(
            user_repository=user_repository,
        ),
        company_service=CompanyService(
            company_repository=company_repository, account_repository=account_repository
        ),
        match_service=MatchService(match_repository=match_repository),
    )


def handle_response_status_code(
    response: Response, core_response: CoreResponse
) -> None:
    response.status_code = STATUS_HTTP_MAPPING[core_response.status]

    if response.status_code // 100 != 2:
        raise HTTPException(
            status_code=response.status_code, detail=core_response.status.value
        )


@app.get("/users/me")
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
) -> Account:
    return application_context.get_current_user(token)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    user = application_context.authenticate_user(form_data.username, form_data.password)
    access_token = application_context.create_access_token(account=user)

    return Token(access_token=access_token, token_type="bearer")


# TODO document response codes for other api methods
@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
    response_model=Account,
)
def register(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    account_response = core.register(
        RegisterRequest(form_data.username, form_data.password)
    )
    handle_response_status_code(response, account_response)
    return account_response.response_content


# @app.post("/logout")
# def logout(response: Response, token: str, core: Core =
# Depends(get_core)) -> BaseModel:
#     logout_response = core.logout(LogoutRequest(token))
#     handle_response_status_code(response, logout_response)
#     return logout_response.response_content


# TODO: need to change url
@app.get("/user/{username}", response_model=User)
def get_user(
    response: Response,
    username: str,
    core: Core = Depends(get_core),
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    get_user_response = core.get_user(username=username)
    handle_response_status_code(response, get_user_response)
    return get_user_response.response_content


@app.put("/user/update", response_model=User)
async def update_user(
    response: Response,
    update_user_request: UpdateUserRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    core: Core = Depends(get_core),
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    account = application_context.get_current_user(token=token)

    setup_user_response = core.update_user(
        SetupUserRequest(
            account=account,
            user=User(
                username=update_user_request.username,
                education=update_user_request.education,
                skills=update_user_request.skills,
                experience=update_user_request.experience,
                preference=Preference(),
            ),
        )
    )
    handle_response_status_code(response, setup_user_response)
    return setup_user_response.response_content


@app.put("/preferences/update", response_model=User)
async def update_preferences(
    response: Response,
    update_preferences_request: UpdatePreferencesRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    core: Core = Depends(get_core),
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    account = application_context.get_current_user(token=token)

    update_preferences_response = core.update_preferences(
        account=account, request=update_preferences_request
    )
    handle_response_status_code(response, update_preferences_response)
    return update_preferences_response.response_content


@app.post("/application", response_model=ApplicationId)
async def create_application(
    response: Response,
    request: CreateApplicationRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    core: Core = Depends(get_core),
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    """
    - Creates application
    - Returns application id for subsequent requests
    """
    account = application_context.get_current_user(token)

    create_application_response = core.create_application(
        account=account, request=request
    )

    handle_response_status_code(response, create_application_response)
    return create_application_response.response_content


@app.get("/application/{application_id}", response_model=Application)
async def get_application(
    response: Response,
    application_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    core: Core = Depends(get_core),
    application_context: IApplicationContext = Depends(get_application_context),
) -> BaseModel:
    """
    - Obtains application with application id
    """
    account = application_context.get_current_user(token)

    get_application_response = core.get_application(
        GetApplicationRequest(account=account, id=application_id)
    )

    handle_response_status_code(response, get_application_response)
    return get_application_response.response_content


@app.put("/application/{application_id}/update")
async def update_application(
    response: Response,
    application_id: int,
    request: UpdateApplicationRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Update application
    """
    account = application_context.get_current_user(token)

    update_application_response = core.update_application(
        account=account, request=request
    )

    handle_response_status_code(response, update_application_response)
    return update_application_response.response_content


@app.put("/application/{application_id}/interaction")
async def application_interaction(
    response: Response,
    application_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Saves interaction with application
    """
    account = application_context.get_current_user(token)

    application_interaction_response = core.application_interaction(
        ApplicationInteractionRequest(id=application_id, account=account)
    )

    handle_response_status_code(response, application_interaction_response)
    return application_interaction_response.response_content


@app.get("/company/{company_id}/application")
def get_company_applications(
    response: Response, company_id: int, core: Core = Depends(get_core)
) -> BaseModel:
    applications_response = core.get_applications(company_id)
    handle_response_status_code(response, applications_response)

    return applications_response.response_content


@app.delete("/application/{application_id}")
async def delete_application(
    response: Response,
    application_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Deletes application
    """
    account = application_context.get_current_user(token)
    delete_application_response = core.delete_application(
        DeleteApplicationRequest(account=account, id=application_id)
    )

    handle_response_status_code(response, delete_application_response)
    return delete_application_response.response_content


@app.get("/industry", responses={200: {}})
def get_industries() -> list[str]:
    return [e for e in Industry]


@app.get("/job_location", responses={200: {}})
def get_job_locations() -> list[str]:
    return [j.value for j in JobLocation]


@app.get("/job_type", responses={200: {}})
def get_job_types() -> list[str]:
    return [j.value for j in JobType]


@app.get("/experience_level", responses={200: {}})
def get_experience_level() -> list[str]:
    return [e.value for e in ExperienceLevel]


@app.get("/organization-size", responses={200: {}})
def get_organization_sizes() -> list[str]:
    return [e for e in OrganizationSize]


@app.get("/experience-level", responses={200: {}})
def get_experience_levels() -> list[str]:
    return [e for e in ExperienceLevel]


@app.post(
    "/company",
    responses={
        200: {},
        401: {},
        500: {},
    },
    response_model=Company,
)
def create_company(
    response: Response,
    request: CreateCompanyRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Registers company
    - Returns created company
    """
    account = application_context.get_current_user(token=token)
    company_response = core.create_company(
        account=account,
        name=request.name,
        website=request.website,
        industry=request.industry,
        organization_size=request.organization_size,
        image_uri=request.image_uri,
        cover_image_uri=request.cover_image_uri,
    )
    handle_response_status_code(response, company_response)
    return company_response.response_content


@app.get(
    "/company/{company_id}",
    responses={
        200: {},
        404: {},
    },
    response_model=Company,
)
def get_company(
    _: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    company_id: int,
    core: Core = Depends(get_core),
) -> BaseModel:
    company_response = core.get_company(company_id=company_id)
    handle_response_status_code(response, company_response)
    return company_response.response_content


@app.put(
    "/company/{company_id}",
    responses={
        200: {},
        404: {},
        500: {},
    },
    response_model=Company,
)
def update_company(
    response: Response,
    company_id: int,
    request: CreateCompanyRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    account = application_context.get_current_user(token)

    company_response = core.update_company(
        account=account,
        company_id=company_id,
        name=request.name,
        website=request.website,
        industry=request.industry,
        organization_size=request.organization_size,
        image_uri=request.image_uri,
        cover_image_uri=request.cover_image_uri,
    )
    handle_response_status_code(response, company_response)

    return company_response.response_content


@app.delete(
    "/company/{company_id}",
    responses={200: {}, 404: {}, 500: {}},
)
def delete_company(
    response: Response,
    company_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> None:
    account = application_context.get_current_user(token)
    delete_response = core.delete_company(account=account, company_id=company_id)
    handle_response_status_code(response, delete_response)


@app.get(
    "/swipe/list/users", responses={200: {}, 404: {}}, response_model=SwipeListResponse
)
def swipe_list_users(
    response: Response,
    swiper_application_id: int,
    amount: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    _ = application_context.get_current_user(token)
    swipe_response = core.get_swipe_list_users(
        swiper_application_id=swiper_application_id, amount=amount
    )
    handle_response_status_code(response, swipe_response)
    return swipe_response.response_content


@app.get(
    "/swipe/list/applications",
    responses={200: {}, 404: {}},
    response_model=SwipeListResponse,
)
def swipe_list_applications(
    response: Response,
    amount: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> BaseModel:
    account = application_context.get_current_user(token)
    swipe_response = core.get_swipe_list_applications(account=account, amount=amount)
    handle_response_status_code(response, swipe_response)
    return swipe_response.response_content


@app.put("/swipe/application")
def swipe_application(
    response: Response,
    request: SwipeApplicationRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> None:
    account = application_context.get_current_user(token)
    swipe_response = core.swipe_application(
        swiper_username=account.username,
        application_id=request.application_id,
        direction=request.direction,
    )
    handle_response_status_code(response, swipe_response)


@app.put("/swipe/user")
def swipe_user(
    response: Response,
    request: SwipeUserRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    application_context: IApplicationContext = Depends(get_application_context),
    core: Core = Depends(get_core),
) -> None:
    _ = application_context.get_current_user(token)
    swipe_response = core.swipe_user(
        swiper_application_id=request.application_id,
        swiped_username=request.swiped_username,
        direction=request.direction,
    )
    handle_response_status_code(response, swipe_response)
