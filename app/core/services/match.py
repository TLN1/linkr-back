from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Preference, SwipeDirection, SwipeFor, SwipeList
from app.core.repository.match import IMatchRepository


@dataclass
class MatchService:
    match_repository: IMatchRepository

    def get_swipe_list(
        self, swipe_for: SwipeFor, amount: int, preference: Preference
    ) -> tuple[Status, SwipeList]:
        swipe_list = self.match_repository.get_swipe_list(
            swipe_for=swipe_for, amount=amount, preference=preference
        )
        return Status.OK, SwipeList(swipe_list=swipe_list)

    def swipe_application(
        self, swiper_username: str, application_id: int, direction: SwipeDirection
    ) -> Status:
        self.match_repository.swipe(
            username=swiper_username,
            application_id=application_id,
            direction=direction,
            swipe_for=SwipeFor.APPLICATION,
        )
        return Status.OK

    def swipe_user(
        self,
        swiper_application_id: int,
        swiped_username: str,
        direction: SwipeDirection,
    ) -> Status:
        self.match_repository.swipe(
            username=swiped_username,
            application_id=swiper_application_id,
            direction=direction,
            swipe_for=SwipeFor.USER,
        )
        return Status.OK
