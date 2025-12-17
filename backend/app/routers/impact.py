from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Edge

router = APIRouter(prefix="/impact", tags=["impact"])


@router.get("/")
def impact(file_path: str, db: Session = Depends(get_db)):
    edges = db.query(Edge).filter(Edge.from_path == file_path).all()

    impacted = [e.to_path for e in edges]

    return {
        "file": file_path,
        "impacted": impacted,
    }
