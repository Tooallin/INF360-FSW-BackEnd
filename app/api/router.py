from fastapi import APIRouter
from app.api.endpoints import conversation, user, message, test

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(conversation.router, prefix="/conversation", tags=["Conversation"])
api_router.include_router(message.router, prefix="/message", tags=["Message"])
api_router.include_router(test.router, prefix="/test", tags=["Testing"])