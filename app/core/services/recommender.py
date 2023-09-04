import pandas as pd
import numpy as np

from dataclasses import dataclass


@dataclass
class Recommender:

    def sort_by_relevance(self, liked, jobs):
        liked = pd.DataFrame(data=liked)
        jobs = pd.DataFrame(data=jobs)
        cols = ['industry', 'job_location', 'job_type', 'experience_level']
        jobs['similarity'] = 0
        for i in range(liked.shape[0]):
            jobs['similarity'] += np.dot(jobs[cols], liked[cols].iloc[i]) / (
                    np.linalg.norm(jobs[cols], axis=1) * np.linalg.norm(liked[cols].iloc[i]))
        return jobs.sort_values(by='similarity', ascending=False)['name'].tolist()


