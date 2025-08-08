from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.chat import ChatCreate, ChatOut
from app.services.conversation import create, get_all
from typing import List
from sqlalchemy.orm import Session
from app.utils.jwt_decode import get_id

router = APIRouter()

# Crear chat para un usuario autenticado
@router.post("/create", response_model=ChatOut)
def Create(chat: ChatCreate, db: Session = Depends(deps.get_db), id_user: int = Depends(get_id)):
	return create(chat=chat, db=db, id_user=id_user)

# Obtener todos los chats para un usuario autenticado
@router.get("/getall", response_model=List[ChatOut])
def GetAll(db: Session = Depends(deps.get_db), id_user: int = Depends(get_id)):
	return get_all(db=db, id_user=id_user)