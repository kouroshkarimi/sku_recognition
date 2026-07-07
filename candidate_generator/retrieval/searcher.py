from pathlib import Path

from PIL import Image

from candidate_generator.embedding.extractor import EmbeddingExtractor
from candidate_generator.retrieval.faiss_index import FaissIndex


class Searcher:

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

        image = Image.open(image_path).convert("RGB")

        embedding = self.extractor.encode(image)

        return self.index.search(
            embedding,
            top_k=top_k,
        )