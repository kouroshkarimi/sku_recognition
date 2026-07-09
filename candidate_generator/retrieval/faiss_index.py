'''
This module implements a Faiss index for efficient similarity search of embeddings.
It provides methods to build, save, load, and search the index.
'''
from pathlib import Path

import faiss
import numpy as np


class FaissIndex:
    '''
    A wrapper around the FAISS index for efficient similarity search of embeddings.
    '''
    def __init__(self, embedding_dim: int):

        self.embedding_dim = embedding_dim

        # cosine similarity (embeddings are already normalized)
        self.index = faiss.IndexFlatIP(embedding_dim)

    def build(self, embeddings: np.ndarray):
        '''
        Build the FAISS index from the provided embeddings.
        Args:
            embeddings (np.ndarray): A 2D array of shape (num_embeddings, embedding_dim).
        '''
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)

        self.index.add(embeddings)

    def save(self, output_path: Path):
        '''
        Save the FAISS index to the specified path.
        Args:
            output_path (Path): The path to save the index file.
        '''
        faiss.write_index(self.index, str(output_path))

    def load(self, index_path: Path):
        '''
        Load a FAISS index from the specified path.
        Args:
            index_path (Path): The path to the index file.
        '''
        self.index = faiss.read_index(str(index_path))

    def search(
        self,
        embedding: np.ndarray,
        top_k: int = 5,
    ):
        '''
        Search the FAISS index for the top-k most similar embeddings to the provided embedding.
        Args:
            embedding (np.ndarray): A 1D or 2D array of shape (embedding_dim,)
              or (1, embedding_dim).
            top_k (int): The number of top similar embeddings to retrieve.
        Returns:
            scores (np.ndarray): The similarity scores of the top-k embeddings.
            indices (np.ndarray): The indices of the top-k embeddings in the index.'''
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        scores, indices = self.index.search(
            embedding.astype(np.float32),
            top_k,
        )

        return scores[0], indices[0]
