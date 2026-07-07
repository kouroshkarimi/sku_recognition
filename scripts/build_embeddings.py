from pathlib import Path
from candidate_generator.database.repository import MetadataRepository
from candidate_generator.database.database import Database
from candidate_generator.embedding.builder import EmbeddingBuilder
from candidate_generator.embedding.dinov2 import DinoV2Embedding
from candidate_generator.embedding.extractor import EmbeddingExtractor

PROJECT_ROOT = Path("__file__").resolve().parent
print(PROJECT_ROOT)

database_path = PROJECT_ROOT / "data" / "metadata" / "gallery.db"
embeddings_path = PROJECT_ROOT / "data" / "embedding"

# Save to database
database = Database(database_path)
repository = MetadataRepository(database)
image_paths_list = repository.get_image_paths()


model = DinoV2Embedding()
extractor = EmbeddingExtractor(model)
builder = EmbeddingBuilder(extractor)

builder.build(
    image_paths=image_paths_list,
    output_dir=embeddings_path,
)

