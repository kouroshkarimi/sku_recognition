'''
This script builds a FAISS index for the embeddings generated from the images in the gallery.
The FAISS index allows for efficient similarity search and retrieval of the top-K candidates
'''
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from candidate_generator.retrieval.faiss_index import FaissIndex

# Embedding directory
embedding_dir = Path("data/embedding")

# Load embeddings
embeddings = np.load(
    embedding_dir / "embeddings.npy"
)

# Build FAISS index
index = FaissIndex(
    embedding_dim=embeddings.shape[1]
)
index.build(embeddings)

# Save FAISS index
index.save(
    embedding_dir / "gallery.index"
)

print("FAISS index saved.")
