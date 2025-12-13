from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class IndexStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"


class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(Text, nullable=False)
    last_indexed_at = Column(DateTime)

    index_jobs = relationship("IndexJob", back_populates="repo")


class IndexJob(Base):
    __tablename__ = "index_jobs"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    status = Column(Enum(IndexStatus), default=IndexStatus.PENDING)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    repo = relationship("Repo", back_populates="index_jobs")


class NodeType(str, enum.Enum):
    FUNCTION = "function"
    CLASS = "class"


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    node_type = Column(Enum(NodeType))
    name = Column(String)
    file_path = Column(Text)
    start_line = Column(Integer)
    end_line = Column(Integer)


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    file_path = Column(Text)
    content = Column(Text)
    symbol_name = Column(String)


class EdgeType(str, enum.Enum):
    CALLS = "calls"


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    from_node_id = Column(Integer)
    to_node_id = Column(Integer)
    edge_type = Column(Enum(EdgeType))
