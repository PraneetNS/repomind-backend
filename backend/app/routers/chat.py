from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openai import OpenAI
from ..deps import get_db, get_settings
from ..models import Chunk

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat(payload: dict, db: Session = Depends(get_db)):
    chunks = db.query(Chunk).filter(Chunk.repo_id == payload["repo_id"]).limit(5).all()
    context = "\n".join(c.content for c in chunks)

    client = OpenAI(api_key=get_settings().OPENAI_API_KEY)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer using the code context."},
            {"role": "user", "content": context + "\n\nQuestion: " + payload["question"]}
        ]
    )

    return {"answer": res.choices[0].message.content}
