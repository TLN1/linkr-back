from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from sqlite3 import Connection, Cursor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = Path(BASE_DIR).joinpath("..").joinpath("app.db")


@dataclass
class ConnectionProvider:
    _connection: Connection | None = field(default=None, init=False)

    @classmethod
    def get_connection(cls) -> Connection:
        if cls._connection is None:
            cls._connection = sqlite3.connect(DB_PATH, check_same_thread=False)

        return cls._connection


def create_tables(cursor: Cursor, connection: Connection) -> None:
    cursor.execute("DROP TABLE IF EXISTS account;")
    cursor.execute("DROP TABLE IF EXISTS company;")
    cursor.execute("DROP TABLE IF EXISTS application;")
    cursor.execute("DROP TABLE IF EXISTS swipe;")
    cursor.execute("DROP TABLE IF EXISTS user;")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS account
        (username TEXT PRIMARY KEY,
         password TEXT);
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            education TEXT,
            skills TEXT,
            experience TEXT,
            account_id INTEGER,
            FOREIGN KEY (account_id) REFERENCES account(id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS company
        (id INTEGER PRIMARY KEY,
         company_name TEXT,
         website TEXT,
         industry TEXT,
         organization_size INTEGER,
         image_uri TEXT,
         cover_image_uri TEXT,
         owner_username TEXT,
         FOREIGN KEY (owner_username) REFERENCES account (username) ON DELETE CASCADE);
       """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS application
        (id INTEGER PRIMARY KEY,
         title TEXT,
         location TEXT,
         job_type TEXT,
         experience_level TEXT,
         description TEXT,
         skills TEXT,
         views INTEGER,
         company_id INTEGER,
         FOREIGN KEY (company_id) REFERENCES company (id) ON DELETE CASCADE);
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS swipe
        (id INTEGER PRIMARY KEY,
         username TEXT,
         application_id INTEGER,
         swipe_for TEXT,
         direction TEXT,
         FOREIGN KEY (username) REFERENCES user (username),
         FOREIGN KEY (application_id) REFERENCES application (id));
        """
    )

    connection.commit()


def main() -> None:
    connection = ConnectionProvider.get_connection()
    cursor = connection.cursor()
    create_tables(cursor, connection)
    connection.close()


if __name__ == "__main__":
    main()
