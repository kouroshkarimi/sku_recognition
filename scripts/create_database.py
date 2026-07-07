from pathlib import Path

from sku_recognition.database.schema import SchemaManager
from sku_recognition.database.database import Database
from sku_recognition.database.repository import MetadataRepository
from sku_recognition.gallery.scanner import GalleryScanner

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