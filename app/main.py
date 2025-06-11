from fastapi import FastAPI
from app.api.endpoints import user, chat
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])