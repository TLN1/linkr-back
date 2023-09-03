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
            [SwipeFor.USER, SwipeDirection.RIGHT, amount, application_id],
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
        return []

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
