from dataclasses import dataclass
from typing import Callable

from app.core.constants import Status
from app.core.models import Account
from app.core.repository.account import IAccountRepository


@dataclass
class AccountService:
    account_repository: IAccountRepository
    hash_function: Callable[[str], str]

    def register(self, username: str, password: str) -> tuple[Status, Account | None]:
        if self.account_repository.has_account(username=username):
            return Status.ACCOUNT_ALREADY_EXISTS, None

        account = self.account_repository.create_account(
            username=username, password=self.hash_function(password)
        )

        status = Status.ACCOUNT_REGISTER_ERROR if account is None else Status.OK

        return status, account
