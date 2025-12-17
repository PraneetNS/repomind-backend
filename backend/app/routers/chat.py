from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.llm import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(payload: dict, db: Session = Depends(get_db)):
    question = payload["question"]
    context = payload.get("context", "")
    
    prompt = f"""
You are an expert software engineer.

Context:
{context}

Question:
{question}
"""
    answer = generate_answer(prompt)
    return {"answer": answer}
