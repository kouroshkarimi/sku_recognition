from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from PIL import Image

from sku_recognition.embedding.dinov2 import DinoV2Embedding
from sku_recognition.embedding.extractor import EmbeddingExtractor
from sku_recognition.retrieval.faiss_index import FaissIndex

from matcher.gim_client import GIMClient


def main():

    
    # Query image
    query_image = Path(
        "data/test_images/sku_013_test.jpg"
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
    
    best_match = gim_client.match(
        query=query_image,
        candidates=candidate_paths,
    )


if __name__ == "__main__":
    main()