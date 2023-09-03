from dataclasses import dataclass
from sqlite3 import Connection

from app.core.models import Application, Preference, SwipeDirection, SwipeFor, User
from app.core.repository.match import IMatchRepository


@dataclass
class SqliteMatchRepository(IMatchRepository):
    connection: Connection

    def get_swipe_list_users(self, application_id: int, amount: int) -> list[User]:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT (u.username, u.education, u.experience, u.skills)
              FROM user u
              LEFT JOIN swipe s on u.username = s.username
             WHERE (s.swipe_for IS NULL AND s.direction IS NULL)
            OR NOT (s.swipe_for == ? AND s.direction == ? AND s.application_id = ?)
             ORDER BY random()
             LIMIT ?;
            """,
            [SwipeFor.USER, SwipeDirection.RIGHT, application_id, amount],
        )

        result = []

        for username, education, experience, skills in res.fetchall():
            # TODO: add preferences if needed :)
            user = User(
                username=username,
                education=education,
                experience=experience,
                skills=skills,
            )

            result.append(user)

        cursor.close()
        return result

    def get_swipe_list_applications(
        self, swiper_username: str, preference: Preference, amount: int
    ) -> list[Application]:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT (a.id, a.title, a.location, a.job_type, a.experience_level,
                    a.description, a.skills, a.views, a.company_id)
              FROM application a
              LEFT JOIN swipe s on a.id = s.application_id
             WHERE (
                    (s.swipe_for IS NULL AND s.direction IS NULL)
                    OR NOT (s.swipe_for == ? AND s.direction == ? AND s.username = ?)
                   )
               AND a.experience_level = ?
               AND a.job_type = ?
               AND a.location = ?
             ORDER BY random()
             LIMIT ?;
            """,
            [
                SwipeFor.APPLICATION,
                SwipeDirection.RIGHT,
                swiper_username,
                preference.experience_level,
                preference.job_type,
                preference.job_location,
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
                skills=skills,
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

        cursor.execute(
            """
            INSERT INTO swipe (username, application_id, swipe_for, direction)
            VALUES (?, ?, ?, ?);
            """,
            (username, application_id, swipe_for, direction),
        )

        self.connection.commit()
        cursor.close()
