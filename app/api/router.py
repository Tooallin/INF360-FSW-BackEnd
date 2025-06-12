from fastapi import APIRouter
from app.api.endpoints import user, chat, message

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(message.router, prefix="/message", tags=["Message"])