import faiss
import numpy as np
from sqlalchemy.orm import Session

from ..models import Chunk
from ..embeddings import generate_embedding

DIMENSION = 384  # all-MiniLM-L6-v2

class VectorIndex:
    def __init__(self):
        self.index = faiss.IndexFlatL2(DIMENSION)
        self.chunk_ids: list[int] = []

    def build(self, db: Session):
        self.index.reset()
        self.chunk_ids.clear()

        chunks = db.query(Chunk).all()

        for chunk in chunks:
            embedding = generate_embedding(chunk.content)
            vector = np.array([embedding]).astype("float32")

            self.index.add(vector)
            self.chunk_ids.append(chunk.id)

    def search(self, query: str, top_k: int = 5) -> list[int]:
        query_vec = np.array(
            [generate_embedding(query)]
        ).astype("float32")

        _, indices = self.index.search(query_vec, top_k)

        return [
            self.chunk_ids[i]
            for i in indices[0]
            if i < len(self.chunk_ids)
        ]


vector_index = VectorIndex()
