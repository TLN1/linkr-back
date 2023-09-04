from dataclasses import dataclass

from app.core.repository.match import IMatchRepository
from app.core.services.recommender import Recommender


@dataclass
class RecommenderService:
    recommender: Recommender
    match_repository: IMatchRepository

    def get_recommendations(self, username: str) -> list[str]:
        jobs = self.match_repository.get_swipe_list_users(username=username, amount=10000)
        liked = self.match_repository.get_right_swiped_list_users(username=username)
        recommendations = self.recommender.get_recommendations(username=username)
        return recommendations
