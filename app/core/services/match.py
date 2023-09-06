from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Application, Preference, SwipeDirection, SwipeFor, User
from app.core.repository.match import IMatchRepository
from app.core.services.recommender_service import RecommenderService


@dataclass
class MatchService:
    match_repository: IMatchRepository
    recommender_service: RecommenderService = RecommenderService()

    def get_swipe_list_users(
        self, swiper_application_id: int, amount: int
    ) -> tuple[Status, list[User]]:
        swipe_list = self.match_repository.get_swipe_list_users(
            application_id=swiper_application_id, amount=amount
        )
        return Status.OK, swipe_list

    def get_right_swiped_list_applications(
        self, swiper_username: str,
    ) -> tuple[Status, list[Application]]:
        swipe_list = self.match_repository.get_right_swiped_list_applications(
            username=swiper_username
        )
        return Status.OK, swipe_list

    def get_swipe_list_applications(
        self, swiper_username: str, preference: Preference, amount: int
    ) -> tuple[Status, list[Application]]:
        swipe_list = self.match_repository.get_swipe_list_applications(
            swiper_username=swiper_username, preference=preference, amount=10000
        )
        right_swiped_list = self.get_right_swiped_list_applications(swiper_username)[1]
        swipe_list_from_recommender = self.recommender_service.get_recommendations(username=swiper_username, swipe_list=swipe_list,
                                                                  right_swiped_list=right_swiped_list)
        if len(swipe_list_from_recommender):
            return Status.OK, swipe_list[:amount]
        swipe_list = self.match_repository.get_swipe_list_applications(
            swiper_username=swiper_username, preference=preference, amount=amount
        )
        return Status.OK, swipe_list

    # Return true if matched, otherwise return false
    def swipe_application(
        self, swiper_username: str, application_id: int, direction: SwipeDirection
    ) -> tuple[Status, bool]:
        self.match_repository.swipe(
            username=swiper_username,
            application_id=application_id,
            direction=direction,
            swipe_for=SwipeFor.APPLICATION,
        )

        matched = direction == SwipeDirection.RIGHT and self.match_repository.matched(
            username=swiper_username, application_id=application_id
        )
        return Status.OK, matched

    # Return true if matched, otherwise return false
    def swipe_user(
        self,
        swiper_application_id: int,
        swiped_username: str,
        direction: SwipeDirection,
    ) -> tuple[Status, bool]:
        self.match_repository.swipe(
            username=swiped_username,
            application_id=swiper_application_id,
            direction=direction,
            swipe_for=SwipeFor.USER,
        )

        matched = direction == SwipeDirection.RIGHT and self.match_repository.matched(
            username=swiped_username, application_id=swiper_application_id
        )
        return Status.OK, matched
