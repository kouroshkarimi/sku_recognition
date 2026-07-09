'''
This script creates the SQLite database for the gallery metadata and 
populates it with data from the gallery directory.
It scans the gallery directory for SKU images, extracts their metadata,
 and saves it to the database.
'''

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from candidate_generator.database.schema import SchemaManager
from candidate_generator.database.database import Database
from candidate_generator.database.repository import MetadataRepository
from candidate_generator.gallery.scanner import GalleryScanner


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
