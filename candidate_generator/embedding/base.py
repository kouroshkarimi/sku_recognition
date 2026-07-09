'''
This module defines the BaseEmbeddingModel abstract class,
which serves as an interface for embedding models used in the SKU recognition system.
'''
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


    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Dimension of the output embedding."""
