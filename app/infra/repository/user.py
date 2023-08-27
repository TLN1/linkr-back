import json
from dataclasses import dataclass, field
from sqlite3 import Connection

from app.core.models import User
from app.core.repository.user import IUserRepository


@dataclass
class InMemoryUserRepository(IUserRepository):
    users: dict[str, User] = field(default_factory=dict)

    def create_user(self, username: str) -> User | None:
        self.users[username] = User(username=username)
        return self.users[username]

    def update_user(self, username: str, user: User) -> User | None:
        if not self.has_user(username=username):
            return None
        self.users[username].update(
            user.education, user.skills, user.experience, user.preference
        )
        return user

    def get_user(self, username: str) -> User | None:
        return self.users.get(username)

    def has_user(self, username: str) -> bool:
        return username in self.users


@dataclass
class SqliteUserRepository(IUserRepository):
    connection: Connection

    def _deserialize_lists(self, user_data):
        user_data["education"] = json.loads(user_data["education"])
        user_data["skills"] = json.loads(user_data["skills"])
        user_data["experience"] = json.loads(user_data["experience"])
        return user_data

    def create_user(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO user (username, education, skills, experience) "
            "VALUES (?, ?, ?, ?)",
            (username, "[]", "[]", "[]"),
        )
        self.connection.commit()
        return User(username=username)

    def update_user(self, username: str, user: User) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE user SET education = ?, skills = ?, experience = ? "
            "WHERE username = ?",
            (
                json.dumps(user.education),
                json.dumps(user.skills),
                json.dumps(user.experience),
                username,
            ),
        )
        self.connection.commit()
        return user

    def get_user(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if user_data:
            user_data = self._deserialize_lists(dict(user_data))
            return User(**user_data)
        return None

    def has_user(self, username: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,))
        return cursor.fetchone()[0] > 0