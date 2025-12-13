from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Repo, IndexJob
from ..services.indexer import index_repo

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/")
def list_repos(db: Session = Depends(get_db)):
    return db.query(Repo).all()

@router.post("/")
def create_repo(payload: dict, db: Session = Depends(get_db)):
    repo = Repo(name=payload["name"], path=payload["path"])
    db.add(repo)
    db.commit()
    db.refresh(repo)

    job = IndexJob(repo_id=repo.id)
    db.add(job)
    db.commit()

    index_repo(db, repo, job)
    return repo
