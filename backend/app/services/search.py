from sqlalchemy.orm import Session
from ..models import Chunk
from ..embeddings import generate_embedding
import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_chunks(db: Session, query: str, limit: int = 5):
    query_embedding = generate_embedding(query)

    chunks = db.query(Chunk).all()
    scored = []

    chunks = (
        db.query(Chunk)
        .filter(Chunk.repo_id == repo_id)
        .filter(Chunk.embedding.isnot(None))
        .all()
    )

    for c in chunks:
        if c.embedding is None:
            continue
        score = cosine_similarity(query_embedding, c.embedding)
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]
