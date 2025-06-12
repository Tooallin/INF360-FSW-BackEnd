from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.chat import ChatCreate, ChatOut
from app.services.chat import create, get_all
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", response_model=ChatOut)
def Create(chat: ChatCreate, db: Session = Depends(deps.get_db)):
	return create(chat=chat, db=db)

@router.get("/getall", response_model=List[ChatOut])
def GetAll(db: Session = Depends(deps.get_db)):
	return get_all(db=db)