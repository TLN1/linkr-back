from dataclasses import dataclass

from app.core.models import Application, JobLocation, JobType, ExperienceLevel
from app.core.repository.match import IMatchRepository
from app.core.services.recommender import Recommender

LOCATIONS = {"On-site": 0, "Remote": 1, "Hybrid": 2}
JOB_TYPES = {"Full-time": 0, "Part-time": 1}
EXPERIENCE_LEVELS = {"Intern": 0, "Junior": 1, "Middle": 2, "Senior": 3, "Lead": 4}

LOCATIONS_ENUMS = {0: JobLocation.ON_SITE, 1: JobLocation.REMOTE, 2: JobLocation.HYBRID}
JOB_TYPES_ENUMS = {0: JobType.FULL_TIME, 1: JobType.PART_TIME}
EXPERIENCE_LEVELS_ENUMS = {
    0: ExperienceLevel.INTERN,
    1: ExperienceLevel.JUNIOR,
    2: ExperienceLevel.MIDDLE,
    3: ExperienceLevel.SENIOR,
    4: ExperienceLevel.LEAD}


# @dataclass
class RecommenderService:
    recommender: Recommender = Recommender()

    def from_application_list_to_dict(self, applications: list[Application]) -> dict[str, list[str | int]]:
        if (len(applications) > 0 ):
            applications_dict: dict[str, list[str | int]] = {i: [] for i in applications[0].__dict__.keys()}
            for application in applications:
                for key, value in application.__dict__.items():
                    if key == 'location':
                        applications_dict[key].append(LOCATIONS[value])
                    elif key == 'job_type':
                        applications_dict[key].append(JOB_TYPES[value])
                    elif key == 'experience_level':
                        applications_dict[key].append(EXPERIENCE_LEVELS[value])
                    else:
                        applications_dict[key].append(value)
            return applications_dict
        return {}

    def from_dict_to_application_list(self, applications_dict: dict[str, list[str | int]]) -> list[Application]:
        applications: list[Application] = []
        for i in range(len(applications_dict['id'])):
            application = Application(
                id=applications_dict['id'][i],
                title=applications_dict['title'][i],
                location=LOCATIONS_ENUMS[applications_dict['location'][i]],
                job_type=JOB_TYPES_ENUMS[applications_dict['job_type'][i]],
                experience_level=EXPERIENCE_LEVELS_ENUMS[applications_dict['experience_level'][i]],
                skills=applications_dict['skills'][i],
                description=applications_dict['description'][i],
                company_id=applications_dict['company_id'][i],
                views=applications_dict['views'][i]
            )
            applications.append(application)
        return applications

    def get_recommendations(
            self, username: str, swipe_list: list[Application], right_swiped_list: list[Application]
    ) -> list[Application]:
        liked = self.from_application_list_to_dict(right_swiped_list)
        applications = self.from_application_list_to_dict(swipe_list)
        recommendations = self.recommender.sort_by_relevance(liked, applications)
        if len(recommendations):
            return self.from_dict_to_application_list(recommendations)
        return []
