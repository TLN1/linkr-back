from typing import Protocol

from app.core.models import Application, Preference, SwipeDirection, SwipeFor, User


class IMatchRepository(Protocol):
    def get_swipe_list_users(self, application_id: int, amount: int) -> list[User]:
        pass

    def get_swipe_list_applications(
        self, swiper_username: str, preference: Preference, amount: int
    ) -> list[Application]:
        pass

    def swipe(
        self,
        username: str,
        application_id: int,
        direction: SwipeDirection,
        swipe_for: SwipeFor,
    ) -> None:
        pass

    def matched(self, username: str, application_id: int) -> bool:
        pass
