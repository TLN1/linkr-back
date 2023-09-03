from dataclasses import dataclass
from sqlite3 import Connection

from app.core.models import Application, Preference, SwipeDirection, SwipeFor, User
from app.core.repository.swipe import IMatchRepository


@dataclass
class SqliteMatchRepository(IMatchRepository):
    connection: Connection

    def _get_swipe_list_users(self, amount: int) -> list[User]:
        cursor = self.connection.cursor()

        res = cursor.execute(
            "SELECT (u.username)"
            "  FROM user u"
            "  LEFT JOIN swipe s on u.username = s.username "
            " WHERE (s.swipe_for IS NULL AND s.direction IS NULL)"
            "    OR NOT (s.swipe_for == ? AND s.direction == ?)"
            " ORDER BY random()"
            " LIMIT ?",
            [SwipeFor.USER, SwipeDirection.RIGHT, amount],
        )

        cursor.close()

    def _get_swipe_list_applications(self, amount: int) -> list[Application]:
        return []

    def get_swipe_list(
        self, swipe_for: SwipeFor, amount: int, preference: Preference
    ) -> list[Application] | list[User]:
        if swipe_for == SwipeFor.USER:
            return self._get_swipe_list_users(amount=amount)
        elif swipe_for == SwipeFor.APPLICATION:
            return self._get_swipe_list_applications(amount=amount)

    def swipe(
        self,
        username: str,
        application_id: int,
        direction: SwipeDirection,
        swipe_for: SwipeFor,
    ) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO swipe "
            "(username, application_id, swipe_for, direction)"
            "VALUES (?, ?, ?, ?)",
            (username, application_id, swipe_for, direction),
        )

        self.connection.commit()
        cursor.close()
