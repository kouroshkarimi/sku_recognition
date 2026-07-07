from __future__ import annotations

from typing import Optional

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from .base import BaseEmbeddingModel
from .transforms import build_transform


class DinoV2Embedding(BaseEmbeddingModel):

    def __init__(
        self,
        model_name: str = "dinov2_vitb14",
        device: Optional[str] = None,
    ):

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = torch.device(device)

        self.model = torch.hub.load(
            "facebookresearch/dinov2",
            model_name,
        )

        self.model.eval()
        self.model.to(self.device)

        self.transform = build_transform()

        self._embedding_dim = {
            "dinov2_vits14": 384,
            "dinov2_vitb14": 768,
            "dinov2_vitl14": 1024,
            "dinov2_vitg14": 1536,
        }[model_name]

    @property
    def embedding_dim(self):

        return self._embedding_dim

    @torch.no_grad()
    def encode(
        self,
        image: Image.Image,
    ) -> np.ndarray:

        if image.mode != "RGB":
            image = image.convert("RGB")

        tensor = self.transform(image)

        tensor = tensor.unsqueeze(0).to(self.device)

        embedding = self.model(tensor)

        embedding = F.normalize(
            embedding,
            p=2,
            dim=1,
        )

        return (
            embedding.squeeze(0)
            .cpu()
            .numpy()
            .astype(np.float32)
        )