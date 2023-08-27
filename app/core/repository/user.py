from typing import Protocol

from app.core.models import User


class IUserRepository(Protocol):
    def create_user(self, username: str) -> User | None:
        pass

    def update_user(self, username: str, user: User) -> User | None:
        pass

    def get_user(self, username: str) -> User | None:
        pass

    def has_user(self, username: str) -> bool:
        pass
