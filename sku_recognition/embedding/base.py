from abc import ABC, abstractmethod
import numpy as np
from PIL import Image


class BaseEmbeddingModel(ABC):
    """Abstract interface for embedding models."""

    @abstractmethod
    def encode(self, image: Image.Image) -> np.ndarray:
        """
        Extract a normalized feature vector from an image.

        Returns
        -------
        np.ndarray
            Shape: (embedding_dim,)
        """
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Dimension of the output embedding."""
        pass