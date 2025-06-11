from fastapi import APIRouter
from app.schemas.message import MessageCreate, MessageOut
from app.services.message import create, get_all
from typing import List

router = APIRouter()

@router.post("/create", response_model=MessageOut)
def Create(message: MessageCreate):
	return create(message=message)

@router.get("/getall/{id_chat}", response_model=List[MessageOut])
def GetAll(id_chat: int):
	return get_all(id_chat=id_chat)