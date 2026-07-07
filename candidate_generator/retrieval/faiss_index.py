from pathlib import Path

import faiss
import numpy as np


class FaissIndex:

    def __init__(self, embedding_dim: int):

        self.embedding_dim = embedding_dim

        # cosine similarity (embeddings are already normalized)
        self.index = faiss.IndexFlatIP(embedding_dim)

    def build(self, embeddings: np.ndarray):

        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)

        self.index.add(embeddings)

    def save(self, output_path: Path):

        faiss.write_index(self.index, str(output_path))

    def load(self, index_path: Path):

        self.index = faiss.read_index(str(index_path))

    def search(
        self,
        embedding: np.ndarray,
        top_k: int = 5,
    ):

        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        scores, indices = self.index.search(
            embedding.astype(np.float32),
            top_k,
        )

        return scores[0], indices[0]