from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import repos, chat, impact

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RepoMind Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repos.router)
app.include_router(chat.router)
app.include_router(impact.router)
