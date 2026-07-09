'''
A class for searching similar embeddings in the FAISS index.
'''
from pathlib import Path

from PIL import Image

from candidate_generator.embedding.extractor import EmbeddingExtractor
from candidate_generator.retrieval.faiss_index import FaissIndex


class Searcher:
    '''
    A class for searching similar embeddings in the FAISS index.
    Attributes:
        extractor (EmbeddingExtractor): An instance of the
          EmbeddingExtractor class for encoding images.
        index (FaissIndex): An instance of the FaissIndex class for searching embeddings.
    '''
    def __init__(
        self,
        extractor: EmbeddingExtractor,
        index_path: Path,
    ):

        self.extractor = extractor

        self.index = FaissIndex(
            embedding_dim=extractor.model.embedding_dim
        )

        self.index.load(index_path)

    def search(
        self,
        image_path: Path,
        top_k: int = 5,
    ):
        '''
        Search for the top-k most similar embeddings to the provided image.
        Args:
            image_path (Path): The path to the query image.
            top_k (int): The number of top similar embeddings to retrieve.
        Returns:
            scores (np.ndarray): The similarity scores of the top-k embeddings.
            indices (np.ndarray): The indices of the top-k embeddings in the index.
        '''
        image = Image.open(image_path).convert("RGB")

        embedding = self.extractor.encode(image)

        return self.index.search(
            embedding,
            top_k=top_k,
        )
