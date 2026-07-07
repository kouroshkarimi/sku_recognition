from pathlib import Path

from .database import Database


class MetadataRepository:

    def __init__(self, database: Database):
        self.database = database

    def insert_gallery(self, skus, images):

        conn = self.database.connect()
        cursor = conn.cursor()

        for sku in skus:

            cursor.execute(
                """
                INSERT OR IGNORE INTO sku(sku_id)
                VALUES(?)
                """,
                (
                    sku["sku_id"],
                )
            )

        for image in images:

            cursor.execute(
                """
                INSERT INTO image(
                    image_id,
                    sku_id,
                    image_path,
                    width,
                    height
                )
                VALUES(?,?,?,?,?)
                """,
                (
                    image["image_id"],
                    image["sku_id"],
                    image["image_path"],
                    image["width"],
                    image["height"]
                )
            )

        conn.commit()
        conn.close()

    def get_image_paths(self) -> list[Path]:
        """
        Returns a list of image paths stored in the database.
        """

        conn = self.database.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT image_path
            FROM image
            ORDER BY image_path
            """
        )

        image_paths = [Path(row[0]) for row in cursor.fetchall()]

        conn.close()

        return image_paths