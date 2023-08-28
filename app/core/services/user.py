from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Account, User, Preference
from app.core.repository.user import IUserRepository


@dataclass
class UserService:
    user_repository: IUserRepository

    def create_user(self, account: Account) -> tuple[Status, User | None]:
        user = self.user_repository.create_user(username=account.username)

        status = Status.USER_SETUP_ERROR if user is None else Status.OK

        return status, user

    def update_user(self, account: Account, user: User) -> tuple[Status, User | None]:
        if account.username != user.username:
            return Status.USER_NOT_FOUND, None

        updated_user = self.user_repository.update_user(
            username=account.username, user=user
        )

        status = Status.USER_SETUP_ERROR if updated_user is None else Status.OK

        return status, updated_user

    def get_user(self, username: str) -> tuple[Status, User | None]:
        if not self.user_repository.has_user(username=username):
            return Status.ACCOUNT_DOES_NOT_EXIST, None

        user = self.user_repository.get_user(username=username)
        return Status.OK, user

    def update_preferences(self, preferences: Preference) -> tuple[Status, User | None]:
        # TODO: implement
        pass
