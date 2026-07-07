from pathlib import Path
import sqlite3


class Database:

    def __init__(self, database_path: Path):

        self.database_path = database_path

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def connect(self) -> sqlite3.Connection:

        connection = sqlite3.connect(self.database_path)

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection