import pandas as pd
import numpy as np

from dataclasses import dataclass

from app.core.models import Application


@dataclass
class Recommender:

    def sort_by_relevance(
            self, liked: dict[str, list[str | int]], applications: dict[str, list[str | int]]
    ) -> dict[str, list[str | int]]:
        liked_df = pd.DataFrame(data=liked)
        applications_df = pd.DataFrame(data=applications)
        cols = ['job_location', 'job_type', 'experience_level']
        applications_df['similarity'] = 0
        for i in range(liked_df.shape[0]):
            applications_df['similarity'] += np.dot(applications_df[cols], liked_df[cols].iloc[i]) / (
                    np.linalg.norm(applications_df[cols], axis=1) * np.linalg.norm(liked_df[cols].iloc[i]))
        return applications_df.sort_values(by='similarity', ascending=False).drop(['similarity'], axis=1).to_dict('list')


