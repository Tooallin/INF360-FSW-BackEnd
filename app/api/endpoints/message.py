from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.message import MessageCreate, MessageOut
from app.services.message import create, get_all, create_base
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", response_model=MessageOut)
def Create(message: MessageCreate, db: Session = Depends(deps.get_db)):
	return create(message=message, db=db)

@router.post("/createbase", response_model=MessageOut)
def CreateBase():
	return create_base()

@router.get("/getall/{id_chat}", response_model=List[MessageOut])
def GetAll(id_chat: int, db: Session = Depends(deps.get_db)):
	return get_all(id_chat=id_chat, db=db)