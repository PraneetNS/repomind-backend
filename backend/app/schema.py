from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import IndexStatus


# ======================
# Repo schemas
# ======================

class RepoCreate(BaseModel):
    name: str
    path: str


class RepoOut(BaseModel):
    id: int
    name: str
    path: str
    last_indexed_at: Optional[datetime] = None
    latest_index_status: Optional[IndexStatus] = None

    class Config:
        from_attributes = True


# ======================
# Index Job schemas
# ======================

class IndexJobOut(BaseModel):
    id: int
    repo_id: int
    status: IndexStatus
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
