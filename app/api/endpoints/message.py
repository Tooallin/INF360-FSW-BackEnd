from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.message import MessageCreate, MessageRead
from app.services.message import create, create_base
from typing import List
from sqlalchemy.orm import Session
from app.utils.jwt_decode import get_id

router = APIRouter()

@router.post("/create", response_model=MessageRead)
def Create(message: MessageCreate, db: Session = Depends(deps.get_db), id_user: int = Depends(get_id)):
	return create(message=message, db=db, id_user=id_user)

@router.get("/createbase", response_model=MessageRead)
def CreateBase(id_user: int = Depends(get_id)):
	return create_base()

"""
@router.get("/getall/{id_chat}", response_model=List[MessageRead])
def GetAll(id_chat: int, db: Session = Depends(deps.get_db), id_user: int = Depends(get_id)):
	return get_all(id_chat=id_chat, db=db, id_user=id_user)
"""