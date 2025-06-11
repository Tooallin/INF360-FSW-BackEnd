from fastapi import APIRouter
from app.schemas.chat import ChatCreate, ChatOut
from app.services.chat import create, get_all
from app.api.endpoints import message
from typing import List

router = APIRouter()

@router.post("/create", response_model=ChatOut)
def Create(chat: ChatCreate):
	return create(chat=chat)

@router.get("/getall", response_model=List[ChatOut])
def GetAll():
	return get_all()

router.include_router(message.router, prefix="/message", tags=["Message"])