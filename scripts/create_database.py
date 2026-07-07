from pathlib import Path

from candidate_generator.database.schema import SchemaManager
from candidate_generator.database.database import Database
from candidate_generator.database.repository import MetadataRepository
from candidate_generator.gallery.scanner import GalleryScanner

PROJECT_ROOT = Path("__file__").resolve().parent
print(PROJECT_ROOT)

database_path = PROJECT_ROOT / "data" / "metadata" / "gallery.db"
gallery_path = PROJECT_ROOT / "data" / "gallery"

# Create database tables
SchemaManager(database_path).create()

# Scan gallery
scanner = GalleryScanner(gallery_path)
skus, images = scanner.scan()


# Save to database
database = Database(database_path)
repository = MetadataRepository(database)
repository.insert_gallery(skus, images)


print("Database created successfully.")