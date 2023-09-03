from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Any

from app.core.models import Application, ExperienceLevel, JobLocation, JobType
from app.core.repository.application import IApplicationRepository


@dataclass
class InMemoryApplicationRepository(IApplicationRepository):
    applications: dict[int, Application] = field(default_factory=dict)
    _application_id: int = 0

    def _next_id(self) -> int:
        self._application_id += 1
        return self._application_id

    def create_application(
        self,
        title: str,
        experience_level: ExperienceLevel,
        location: JobLocation,
        job_type: JobType,
        skills: list[str],
        description: str,
        company_id: int,
    ) -> Application | None:
        application_id = self._next_id()
        application = Application(
            id=application_id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            description=description,
            company_id=company_id,
            views=0,
        )

        self.applications[application_id] = application
        return application

    def get_application(self, id: int) -> Application | None:
        return self.applications.get(id)

    def get_company_applications(self, company_id: int) -> list[Application]:
        return list(
            filter(
                lambda application: application.company_id == company_id,
                self.applications.values(),
            )
        )

    def has_application(self, id: int) -> bool:
        return self.get_application(id=id) is not None

    def update_application(
        self,
        id: int,
        title: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        skills: list[str],
        description: str,
    ) -> Application | None:
        if not self.has_application(id=id):
            return None

        self.applications[id].update(
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            description=description,
        )

        return self.applications[id]

    def application_interaction(self, id: int) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications[id].views += 1
        return True

    def delete_application(self, id: int) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications.pop(id)
        return True


@dataclass
class SqliteApplicationRepository(IApplicationRepository):
    connection: Connection

    @staticmethod
    def _convert_row(row: Any) -> Application | None:
        (
            id,
            title,
            location,
            job_type,
            experience_level,
            description,
            skill_encoded,
            views,
            company_id,
        ) = row

        return Application(
            id=id,
            title=title,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            skills=skill_encoded.split(","),
            description=description,
            views=views,
            company_id=company_id,
        )

    @staticmethod
    def _convert_rows(rows: Any) -> list[Application]:
        result = []

        for row in rows:
            application = SqliteApplicationRepository._convert_row(row=row)

            if application is not None:
                result.append(application)

        return result

    def create_application(
        self,
        title: str,
        experience_level: ExperienceLevel,
        location: JobLocation,
        job_type: JobType,
        skills: list[str],
        description: str,
        company_id: int,
    ) -> Application | None:
        cursor = self.connection.cursor()
        skills_encoded = ",".join(skills)
        res = cursor.execute(
            "INSERT INTO application "
            "(title, location, job_type, experience_level, "
            "description, skills, views, company_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                title,
                location,
                job_type,
                experience_level,
                description,
                skills_encoded,
                0,
                company_id,
            ),
        )

        self.connection.commit()

        if res.rowcount == 0 or res.lastrowid is None:
            cursor.close()
            return None

        res = cursor.execute(
            "SELECT * FROM application WHERE ROWID = ?", [res.lastrowid]
        )

        row = res.fetchone()
        if row is None:
            return None

        cursor.close()
        return SqliteApplicationRepository._convert_row(row=row)

    def get_application(self, id: int) -> Application | None:
        cursor = self.connection.cursor()
        res = cursor.execute("SELECT * FROM application WHERE id = ?", [id])

        row = res.fetchone()
        if row is None:
            return None

        cursor.close()
        return SqliteApplicationRepository._convert_row(row=row)

    def get_company_applications(self, company_id: int) -> list[Application]:
        cursor = self.connection.cursor()

        res = cursor.execute(
            "SELECT * FROM application WHERE company_id = ?", [company_id]
        )

        rows = res.fetchall()
        if rows is None:
            return []

        cursor.close()
        return SqliteApplicationRepository._convert_rows(rows=rows)

    def has_application(self, id: int) -> bool:
        return self.get_application(id=id) is not None

    def update_application(
        self,
        id: int,
        title: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        skills: list[str],
        description: str,
    ) -> Application | None:
        application = self.get_application(id=id)

        if application is None:
            return None
        skills_encoded = ",".join(skills)

        cursor = self.connection.cursor()

        res = cursor.execute(
            "UPDATE application "
            "   SET title = ?, "
            "       location = ?, "
            "       job_type = ?, "
            "       experience_level = ?, "
            "       skills = ?, "
            "       description = ?"
            " WHERE id = ?",
            (
                title,
                str(location),
                str(job_type),
                str(experience_level),
                skills_encoded,
                description,
                id,
            ),
        )

        self.connection.commit()
        cursor.close()

        if res.rowcount == 0:
            return None

        return self.get_application(id=id)

    def application_interaction(self, id: int) -> bool:
        application = self.get_application(id=id)

        if application is None:
            return False

        cursor = self.connection.cursor()

        res = cursor.execute(
            "UPDATE application SET views = ? WHERE id = ?", (application.views + 1, id)
        )

        self.connection.commit()
        cursor.close()

        return res.rowcount != 0

    def delete_application(self, id: int) -> bool:
        cursor = self.connection.cursor()

        res = cursor.execute("DELETE FROM application WHERE id = ?", [id])

        self.connection.commit()
        cursor.close()

        return res.rowcount != 0
