from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Node, Edge

router = APIRouter(prefix="/impact", tags=["impact"])

@router.post("/")
def impact(payload: dict, db: Session = Depends(get_db)):
    node = db.query(Node).filter(
        Node.repo_id == payload["repo_id"],
        Node.name == payload["function_name"]
    ).first()

    if not node:
        return {"error": "Function not found"}

    callers = db.query(Edge).filter(Edge.to_node_id == node.id).all()
    callees = db.query(Edge).filter(Edge.from_node_id == node.id).all()

    return {
        "function": node.name,
        "called_by": [c.from_node_id for c in callers],
        "calls": [c.to_node_id for c in callees]
    }
