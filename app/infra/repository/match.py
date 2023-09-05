import json
from dataclasses import dataclass
from sqlite3 import Connection

from app.core.models import (
    Application,
    Education,
    Experience,
    Preference,
    Skill,
    SwipeDirection,
    SwipeFor,
    User,
)
from app.core.repository.match import IMatchRepository


@dataclass
class SqliteMatchRepository(IMatchRepository):
    connection: Connection

    def get_swipe_list_users(self, application_id: int, amount: int) -> list[User]:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT u.username, u.education, u.experience, u.skills
              FROM user u
              LEFT JOIN swipe s on u.username = s.username
               AND s.application_id = ?
             WHERE (s.swipe_for IS NULL AND s.direction IS NULL)
            OR NOT (s.swipe_for == ? AND s.direction == ?)
             ORDER BY random()
             LIMIT ?;
            """,
            [application_id, SwipeFor.USER, SwipeDirection.RIGHT, amount],
        )

        result = []

        for username, education, experience, skills in res.fetchall():
            education_list = [
                Education(name=edu["name"], description=edu["description"])
                for edu in json.loads(education)
            ]
            skills_list = [
                Skill(name=skill["name"], description=skill["description"])
                for skill in json.loads(skills)
            ]
            experience_list = [
                Experience(name=exp["name"], description=exp["description"])
                for exp in json.loads(experience)
            ]

            # TODO: add preferences if needed :)
            user = User(
                username=username,
                education=education_list,
                experience=experience_list,
                skills=skills_list,
            )

            result.append(user)

        cursor.close()
        return result

    def get_swipe_list_applications(
        self, swiper_username: str, preference: Preference, amount: int
    ) -> list[Application]:
        cursor = self.connection.cursor()

        # TODO: add filtering with preferences
        res = cursor.execute(
            """
            SELECT a.id, a.title, a.location, a.job_type, a.experience_level,
                   a.description, a.skills, a.views, a.company_id
              FROM application a
              LEFT JOIN swipe s on a.id = s.application_id
               AND s.username = ?
             WHERE (
                    (s.swipe_for IS NULL AND s.direction IS NULL)
                    OR NOT (s.swipe_for == ? AND s.direction == ?)
                   )
             ORDER BY random()
             LIMIT ?;
            """,
            [
                swiper_username,
                SwipeFor.APPLICATION,
                SwipeDirection.RIGHT,
                amount,
            ],
        )

        result = []

        for (
            id,
            title,
            location,
            job_type,
            experience_level,
            description,
            skills,
            views,
            company_id,
        ) in res.fetchall():
            application = Application(
                id=id,
                title=title,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                description=description,
                skills=skills.split(","),
                views=views,
                company_id=company_id,
            )

            result.append(application)

        cursor.close()
        return result

    def swipe(
        self,
        username: str,
        application_id: int,
        direction: SwipeDirection,
        swipe_for: SwipeFor,
    ) -> None:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT *
              FROM swipe
             WHERE username = ?
               AND application_id = ?
               AND swipe_for = ?;
            """,
            (username, application_id, swipe_for),
        )

        if res.fetchone() is None:
            cursor.execute(
                """
                INSERT INTO swipe (username, application_id, swipe_for, direction)
                VALUES (?, ?, ?, ?);
                """,
                (username, application_id, swipe_for, direction),
            )
        else:
            cursor.execute(
                """
                UPDATE swipe SET direction = ?
                 WHERE username = ?
                   AND application_id = ?
                   AND swipe_for = ?;
                """,
                (direction, username, application_id, swipe_for),
            )

        self.connection.commit()
        cursor.close()

    def matched(self, username: str, application_id: int) -> bool:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT * FROM swipe
             WHERE username = ?
               AND application_id = ?
               AND direction = ?
               AND swipe_for = ?;
            """,
            [username, application_id, SwipeDirection.RIGHT, SwipeFor.APPLICATION],
        )

        user_liked_application = res.fetchone() is not None

        res = cursor.execute(
            """
            SELECT * FROM swipe
             WHERE username = ?
               AND application_id = ?
               AND direction = ?
               AND swipe_for = ?;
            """,
            [username, application_id, SwipeDirection.RIGHT, SwipeFor.USER],
        )

        application_liked_user = res.fetchone() is not None

        cursor.close()
        return user_liked_application and application_liked_user
