from typing import Protocol

from app.core.models import Account, Application, Company


class IAccountRepository(Protocol):
    def create_account(self, username: str, password: str) -> Account | None:
        pass

    def get_account(self, username: str) -> Account | None:
        pass

    def has_account(self, username: str) -> bool:
        pass

    def is_valid(self, username: str, password: str) -> bool:
        pass

    def link_company(self, username: str, company: Company) -> bool:
        pass

    def link_application(self, username: str, application: Application) -> bool:
        pass
