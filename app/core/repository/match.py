from typing import Protocol

from app.core.models import Application, Preference, SwipeDirection, SwipeFor, User


class IMatchRepository(Protocol):
    def get_swipe_list(
        self, swipe_for: SwipeFor, amount: int, preference: Preference
    ) -> list[Application] | list[User]:
        pass

    def swipe(
        self,
        username: str,
        application_id: int,
        direction: SwipeDirection,
        swipe_for: SwipeFor,
    ) -> None:
        pass
