'''
This module defines the SchemaManager class, which is responsible for creating
the database schema for the SKU recognition system. It provides methods to create
the necessary tables for storing SKU and gallery image information.
The schema includes two tables: "sku" for storing SKU information and "image"
for storing gallery image information. The "image" table has a foreign key
relationship with the "sku" table, linking each gallery image to its corresponding SKU.
'''

from pathlib import Path
from .database import Database

class SchemaManager:
    '''
    SchemaManager is a class that is responsible for creating the database schema
    '''
    def __init__(self, database_path: Path):

        self.database = Database(database_path)

    def create(self):
        '''
        Creates the database schema by creating the necessary tables for storing
        SKU and gallery image information. The schema includes two tables: "sku" for
        storing SKU information and "image" for storing gallery image information.
        Args:
            None
        Returns:
            None
    '''
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
