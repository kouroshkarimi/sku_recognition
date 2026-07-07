from pathlib import Path

import numpy as np

from sku_recognition.retrieval.faiss_index import FaissIndex

embedding_dir = Path("data/embedding")

embeddings = np.load(
    embedding_dir / "embeddings.npy"
)

index = FaissIndex(
    embedding_dim=embeddings.shape[1]
)

index.build(embeddings)

index.save(
    embedding_dir / "gallery.index"
)

print("FAISS index saved.")