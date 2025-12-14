from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.search import search_chunks
from openai import OpenAI

client = OpenAI()
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def chat(query: str, db: Session = Depends(get_db)):
    chunks = search_chunks(db, query)

    context = "\n\n".join(
        f"File: {c.file_path}\n{c.content}" for c in chunks
    )

    prompt = f"""
You are a code assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{query}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return {"answer": res.choices[0].message.content}
