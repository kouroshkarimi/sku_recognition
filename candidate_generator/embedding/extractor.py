from typing import Iterable, List
import numpy as np
from PIL import Image

from .base import BaseEmbeddingModel


class EmbeddingExtractor:

    def __init__(self, model: BaseEmbeddingModel):
        self.model = model

    def encode(self, image: Image.Image) -> np.ndarray:
        return self.model.encode(image)

    def encode_batch(
        self,
        images: Iterable[Image.Image],
    ) -> np.ndarray:
        embeddings = [self.model.encode(img) for img in images]
        return np.stack(embeddings, axis=0)