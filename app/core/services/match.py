from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Preference, SwipeDirection, SwipeFor, SwipeList
from app.core.repository.match import IMatchRepository


@dataclass
class MatchService:
    match_repository: IMatchRepository

    def get_swipe_list_users(
        self, swiper_application_id: int, amount: int
    ) -> tuple[Status, SwipeList]:
        swipe_list = self.match_repository.get_swipe_list_users(
            application_id=swiper_application_id, amount=amount
        )
        return Status.OK, SwipeList(swipe_list=swipe_list)

    def get_swipe_list_applications(
        self, swiper_username: str, preference: Preference, amount: int
    ) -> tuple[Status, SwipeList]:
        swipe_list = self.match_repository.get_swipe_list_applications(
            swiper_username=swiper_username, preference=preference, amount=amount
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
