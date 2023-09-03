from typing import Any, Protocol

from app.core.models import Account


class IApplicationContext(Protocol):
    def authenticate_user(self, username: str, password: str) -> Account:
        pass

    def create_access_token(self, account: Account) -> str:
        pass

    def get_current_user(self, token: Any) -> Account:
        pass

    def logout_user(self, token: str) -> None:
        pass
