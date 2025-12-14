from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema
from ..services.indexer import index_repo

router = APIRouter(prefix="/repos", tags=["repos"])


@router.post("/", response_model=schema.RepoOut)
def create_repo(
    data: schema.RepoCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    repo = models.Repo(name=data.name, path=data.path)
    db.add(repo)
    db.commit()
    db.refresh(repo)

    job = models.IndexJob(repo_id=repo.id)
    db.add(job)
    db.commit()

    # ✅ Run indexing in background
    background_tasks.add_task(index_repo, db, repo, job)

    return repo
@router.get("/", response_model=list[schema.RepoOut])
def list_repos(db: Session = Depends(get_db)):
    repos = db.query(models.Repo).all()

    for r in repos:
        if r.index_jobs:
            r.latest_index_status = r.index_jobs[-1].status
        else:
            r.latest_index_status = models.IndexStatus.PENDING

    return repos
