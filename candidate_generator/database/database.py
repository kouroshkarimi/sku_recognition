'''
This module defines the Database class, which provides methods for
 connecting to a SQLite database.
The Database class is initialized with a database path
and provides a method to connect to the database.
The connect method establishes a connection to
the SQLite database and enables foreign key support.
'''

from pathlib import Path
import sqlite3


class Database:
    '''
    Database is a class that provides methods for connecting to a SQLite database.
    '''
    def __init__(self, database_path: Path):

        self.database_path = database_path

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def connect(self) -> sqlite3.Connection:
        '''
        Connect to the SQLite database and enable foreign key support.
        Returns:
            sqlite3.Connection: A connection object to the SQLite database.
        '''
        connection = sqlite3.connect(self.database_path)

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection
