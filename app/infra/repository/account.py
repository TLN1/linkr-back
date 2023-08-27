from dataclasses import dataclass, field

from app.core.models import Account, Application, Company
from app.core.repository.account import IAccountRepository


@dataclass
class InMemoryAccountRepository(IAccountRepository):
    accounts: dict[str, Account] = field(default_factory=dict)

    def create_account(self, username: str, password: str) -> Account | None:
        account = Account(
            id=len(self.accounts) + 1,
            username=username,
            password=password,
        )

        self.accounts[username] = account
        return account

    def get_account(self, username: str) -> Account | None:
        return self.accounts.get(username)

    def has_account(self, username: str) -> bool:
        return self.get_account(username=username) is not None

    def is_valid(self, username: str, password: str) -> bool:
        return (
            username in self.accounts and self.accounts[username].password == password
        )

    def link_company(self, username: str, company: Company) -> bool:
        account = self.get_account(username)
        if account is None:
            return False

        account.link_company(company)
        return True

    def link_application(self, username: str, application: Application) -> bool:
        account = self.get_account(username)
        if account is None:
            return False

        account.link_application(application)
        return True
