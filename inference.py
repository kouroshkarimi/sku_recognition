"""
Run SKU recognition inference on a query image.

This script extracts a DINOv2 embedding, retrieves Top-K candidates
from the FAISS index, and verifies them using GIM server (local_matching).
"""

from pathlib import Path
import sys
import numpy as np
from PIL import Image

from candidate_generator.embedding.dinov2 import DinoV2Embedding
from candidate_generator.embedding.extractor import EmbeddingExtractor
from candidate_generator.retrieval.faiss_index import FaissIndex
from local_matcher.gim_client import GIMClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


# Query image
query_image = Path(
    "data/test_images/sku_70_test.jpg"
)


# Load DINOv2 (Encoder)
model = DinoV2Embedding()
extractor = EmbeddingExtractor(model)

# Load FAISS
index = FaissIndex(
    embedding_dim=model.embedding_dim
)

index.load(
    Path("data/embedding/gallery.index")
)


# Encode query
image = Image.open(query_image).convert("RGB")
embedding = extractor.encode(image)

# Search
scores, indices = index.search(
    embedding,
    top_k=5,
)

# Load gallery paths
gallery_paths = np.load(
    "data/embedding/paths.npy",
    allow_pickle=True,
)

print()
print("Top-5 Matches")
print("=" * 50)

for rank, (score, idx) in enumerate(zip(scores, indices), start=1):

    print(f"Rank : {rank}")
    print(f"Score: {score:.4f}")
    print(f"Image: {gallery_paths[idx]}")
    print()


candidate_paths = [
    str(gallery_paths[idx])
    for idx in indices
    ]

gim_client = GIMClient()

# Match query image with candidates using GIM server
for candidate_path in candidate_paths:
    print(f"Matching {query_image} with {candidate_path}...")
    match_result = gim_client.match(
        query=str(query_image),
        candidates=str(candidate_path),
    )

    if match_result.json()['score'] > 0:
        print(match_result.json()['candidate_path'])
        print(match_result.json()['score'])
