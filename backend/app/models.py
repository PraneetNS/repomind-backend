from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, PickleType
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


# =========================
# Index job status
# =========================

class IndexStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"


# =========================
# Repo
# =========================

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    path = Column(Text, nullable=False)
    last_indexed_at = Column(DateTime, nullable=True)

    index_jobs = relationship("IndexJob", back_populates="repo")


    @property
    def latest_index_status(self):
        if not self.index_jobs:
            return None
        return self.index_jobs[-1].status


# =========================
# Index job
# =========================

class IndexJob(Base):
    __tablename__ = "index_jobs"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    status = Column(Enum(IndexStatus), default=IndexStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    error_message = Column(Text, nullable=True)

    repo = relationship("Repo", back_populates="index_jobs")


# =========================
# Node graph
# =========================

class NodeType(str, enum.Enum):
    FUNCTION = "function"
    CLASS = "class"
    FILE = "file"
    MODULE = "module"


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    node_type = Column(Enum(NodeType), nullable=False)
    name = Column(String(255), nullable=True)
    file_path = Column(Text, nullable=False)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)

    repo = relationship("Repo")


# =========================
# Chunks
# =========================

class ChunkType(str, enum.Enum):
    CODE = "code"
    DOC = "doc"
    TEST = "test"


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    chunk_type = Column(Enum(ChunkType), nullable=False)
    file_path = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    symbol_name = Column(String(255), nullable=True)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)
    embedding = Column(PickleType, nullable=True)

    repo = relationship("Repo")
class EdgeType(str, enum.Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    DEFINES = "defines"


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    from_node_id = Column(Integer, ForeignKey("nodes.id"))
    to_node_id = Column(Integer, ForeignKey("nodes.id"))
    edge_type = Column(Enum(EdgeType), nullable=False)
class EdgeType(str, enum.Enum):
    IMPORTS = "imports"


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)

    from_path = Column(Text, nullable=False)
    to_path = Column(Text, nullable=False)

    edge_type = Column(Enum(EdgeType), nullable=False)
