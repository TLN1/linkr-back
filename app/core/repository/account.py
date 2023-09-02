from typing import Protocol

from app.core.models import Account


class IAccountRepository(Protocol):
    def create_account(self, username: str, password: str) -> Account | None:
        pass

    def get_account(self, username: str) -> Account | None:
        pass

    def has_account(self, username: str) -> bool:
        pass

    def is_valid(self, username: str, password: str) -> bool:
        pass
