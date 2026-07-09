'''
This script builds embeddings for the images in the gallery and
 saves them to the specified output directory.
It uses the DINOv2 model to extract embeddings for each image.
The embeddings are saved in a format compatible with the FAISS index for efficient retrieval.
'''
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from candidate_generator.database.repository import MetadataRepository
from candidate_generator.database.database import Database
from candidate_generator.embedding.builder import EmbeddingBuilder
from candidate_generator.embedding.dinov2 import DinoV2Embedding
from candidate_generator.embedding.extractor import EmbeddingExtractor


database_path = PROJECT_ROOT / "data" / "metadata" / "gallery.db"
embeddings_path = PROJECT_ROOT / "data" / "embedding"

# Save to database
database = Database(database_path)
repository = MetadataRepository(database)
image_paths_list = repository.get_image_paths()

# Load DINOv2 (Encoder)
model = DinoV2Embedding()
extractor = EmbeddingExtractor(model)
builder = EmbeddingBuilder(extractor)

# Build embeddings
builder.build(
    image_paths=image_paths_list,
    output_dir=embeddings_path,
)
