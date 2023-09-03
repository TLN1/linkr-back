from dataclasses import dataclass, field
from sqlite3 import Connection

from app.core.models import Account
from app.core.repository.account import IAccountRepository
from app.core.repository.company import ICompanyRepository


@dataclass
class InMemoryAccountRepository(IAccountRepository):
    company_repository: ICompanyRepository
    accounts: dict[str, Account] = field(default_factory=dict)

    def create_account(self, username: str, password: str) -> Account | None:
        account = Account(
            username=username,
            password=password,
        )

        self.accounts[username] = account
        return account

    def get_account(self, username: str) -> Account | None:
        account = self.accounts.get(username)

        if account is None:
            return None

        account.companies = self.company_repository.get_user_companies(
            username=username
        )

        return account

    def has_account(self, username: str) -> bool:
        return self.get_account(username=username) is not None

    def is_valid(self, username: str, password: str) -> bool:
        return (
            username in self.accounts and self.accounts[username].password == password
        )


@dataclass
class SqliteAccountRepository(IAccountRepository):
    connection: Connection
    company_repository: ICompanyRepository

    def create_account(self, username: str, password: str) -> Account | None:
        cursor = self.connection.cursor()
        account = Account(username=username, password=password)

        res = cursor.execute(
            "INSERT INTO account (username, password) VALUES (?, ?)",
            (account.username, account.password),
        )

        self.connection.commit()
        cursor.close()

        if res.rowcount == 0:
            return None

        return account

    def get_account(self, username: str) -> Account | None:
        cursor = self.connection.cursor()

        res = cursor.execute("SELECT * FROM account WHERE username = ?", [username])

        row = res.fetchone()
        if row is None:
            return None

        cursor.close()

        username, password = row
        companies = self.company_repository.get_user_companies(username=username)

        return Account(username=username, password=password, companies=companies)

    def has_account(self, username: str) -> bool:
        return self.get_account(username=username) is not None

    def is_valid(self, username: str, password: str) -> bool:
        account = self.get_account(username=username)

        if account is None:
            return False

        return account.username == username and account.password == password
