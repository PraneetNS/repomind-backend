import os, ast
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Repo, IndexJob, IndexStatus, Node, NodeType, Chunk
from ..embeddings import generate_embedding

from ..models import Edge, EdgeType

def index_repo(db: Session, repo: Repo, job: IndexJob):
    job.status = IndexStatus.RUNNING
    db.commit()

    try:
        for root, _, files in os.walk(repo.path):
            for f in files:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    source = file.read()

                tree = ast.parse(source)
                node_map = {}

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        n = Node(
                            repo_id=repo.id,
                            node_type=NodeType.FUNCTION,
                            name=node.name,
                            file_path=path,
                            start_line=node.lineno,
                            end_line=node.end_lineno
                        )
                        db.add(n)
                        db.flush()
                        node_map[node.name] = n.id

                        chunk = Chunk(
                            repo_id=repo.id,
                            file_path=path,
                            content="\n".join(source.splitlines()[node.lineno-1:node.end_lineno]),
                            symbol_name=node.name
                        )
                        db.add(chunk)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        caller = next((p.name for p in ast.walk(tree)
                                      if isinstance(p, ast.FunctionDef)
                                      and p.lineno <= node.lineno <= p.end_lineno), None)
                        if caller and caller in node_map and node.func.id in node_map:
                            #db.add(Edge(
                                #repo_id=repo.id,
                                #from_node_id=node_map[caller],
                                #to_node_id=node_map[node.func.id],
                                #edge_type=EdgeType.CALLS
                            #))

                            repo.last_indexed_at = datetime.utcnow()
                            job.status = IndexStatus.COMPLETED
        db.commit()

    except Exception as e:
        job.status = IndexStatus.FAILED
        job.error_message = str(e)
        db.commit()
        raise
def chunk_text(text: str, max_lines: int = 50):
    lines = text.splitlines()
    for i in range(0, len(lines), max_lines):
        yield "\n".join(lines[i:i + max_lines]), i + 1, min(i + max_lines, len(lines))
