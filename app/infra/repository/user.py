import json
from dataclasses import dataclass, field
from sqlite3 import Connection

from app.core.models import Education, Experience, Preference, Skill, User, Industry, JobType, JobLocation, \
    ExperienceLevel
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
        return self.get_user(username=username) is not None

    def update_preferences(self, username: str, preference: Preference) -> User | None:
        if not self.has_user(username=username):
            return None
        self.users[username].preference = preference
        return self.users[username]


@dataclass
class SqliteUserRepository(IUserRepository):
    connection: Connection

    # def _deserialize_lists(self, user_data):
    #     user_data["education"] = json.loads(user_data["education"])
    #     user_data["skills"] = json.loads(user_data["skills"])
    #     user_data["experience"] = json.loads(user_data["experience"])
    #     return user_data

    def create_user(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO user (username, education, skills, experience, preference) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, json.dumps([]), json.dumps([]), json.dumps([]), json.dumps({
                    "industry": [],
                    "job_type": [],
                    "job_location": [],
                    "experience_level": []
                }))
        )
        self.connection.commit()
        return User(username=username)

    def update_user(self, username: str, user: User) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE user SET education = ?, skills = ?, experience = ? "
            "WHERE username = ?",
            (
                json.dumps(
                    [
                        {"name": edu.name, "description": edu.description}
                        for edu in user.education
                    ]
                ),
                json.dumps(
                    [
                        {"name": skill.name, "description": skill.description}
                        for skill in user.skills
                    ]
                ),
                json.dumps(
                    [
                        {"name": exp.name, "description": exp.description}
                        for exp in user.experience
                    ]
                ),
                username,
            ),
        )
        self.connection.commit()
        return user

    def get_user(self, username: str) -> User | None:
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        username = user_data[1]

        educations = json.loads(user_data[2])
        education_list = [
            Education(name=edu["name"], description=edu["description"])
            for edu in educations
        ]

        skills = json.loads(user_data[3])
        skills_list = [
            Skill(name=skill["name"], description=skill["description"])
            for skill in skills
        ]

        experience = json.loads(user_data[4])
        experience_list = [
            Experience(name=exp["name"], description=exp["description"])
            for exp in experience
        ]

        preference_dict = json.loads(user_data[5])
        preference = Preference(
            industry=[Industry(i) for i in preference_dict["industry"]],
            job_type=[JobType(i) for i in preference_dict["job_type"]],
            job_location=[JobLocation(i) for i in preference_dict["job_location"]],
            experience_level=[ExperienceLevel(i) for i in preference_dict["experience_level"]])
        print(preference.industry)

        return User(
            username=username,
            education=education_list,
            skills=skills_list,
            experience=experience_list,
            preference=preference
        )

    def has_user(self, username: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,))
        user_exists: bool = cursor.fetchone()[0] > 0
        return user_exists

    def update_preferences(self, username: str, preference: Preference) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE user SET preference = ? WHERE username = ?",
            (
                json.dumps(
                    {
                        "industry": preference.industry,
                        "job_type": preference.job_type,
                        "job_location": preference.job_location,
                        "experience_level": preference.experience_level,
                    }
                ),
                username,
            ),
        )
        self.connection.commit()
        return self.get_user(username=username)
