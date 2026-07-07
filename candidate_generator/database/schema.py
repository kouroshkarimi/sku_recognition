from pathlib import Path

from .database import Database


class SchemaManager:

    def __init__(self, database_path: Path):

        self.database = Database(database_path)

    def create(self):

        connection = self.database.connect()

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sku(

            sku_id TEXT PRIMARY KEY,

            name TEXT,

            brand TEXT,

            category TEXT,

            barcode TEXT,

            description TEXT,

            active INTEGER DEFAULT 1

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS image(

            image_id TEXT PRIMARY KEY,

            sku_id TEXT NOT NULL,

            image_path TEXT NOT NULL,

            width INTEGER,

            height INTEGER,

            FOREIGN KEY(sku_id)

                REFERENCES sku(sku_id)

        )
        """)

        connection.commit()

        connection.close()