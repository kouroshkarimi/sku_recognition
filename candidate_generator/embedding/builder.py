from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image
from tqdm import tqdm

from .extractor import EmbeddingExtractor


class EmbeddingBuilder:
    """
    Builds embeddings for a gallery of images and saves them to disk.

    Outputs:
        embeddings.npy : (N, D) float32
        ids.npy        : (N,)
        paths.npy      : (N,)
    """

    def __init__(self, extractor: EmbeddingExtractor):
        self.extractor = extractor

    def build(
        self,
        image_paths: Iterable[Path],
        output_dir: Path,
    ) -> None:

        output_dir.mkdir(parents=True, exist_ok=True)

        embeddings = []
        ids = []
        paths = []

        image_paths = list(image_paths)

        for image_path in tqdm(image_paths, desc="Extracting embeddings"):

            try:
                image = Image.open(image_path).convert("RGB")

                embedding = self.extractor.encode(image)

                embeddings.append(embedding)

                # sku_001, sku_002, ...
                ids.append(image_path.parent.name)

                paths.append(str(image_path))

            except Exception as e:
                print(f"Skipping {image_path}: {e}")

        if len(embeddings) == 0:
            raise RuntimeError("No embeddings were generated.")

        embeddings = np.stack(embeddings).astype(np.float32)

        ids = np.asarray(ids)

        paths = np.asarray(paths)

        np.save(output_dir / "embeddings.npy", embeddings)

        np.save(output_dir / "ids.npy", ids)

        np.save(output_dir / "paths.npy", paths)

        print(f"Saved {len(embeddings)} embeddings")
        print(f"Embedding dimension: {embeddings.shape[1]}")
        print(f"Output directory: {output_dir}")