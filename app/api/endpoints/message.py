from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.message import MessageCreate, MessageRead, MessageIA
from app.services.message import create, create_base, get_all
from typing import List
from sqlalchemy.orm import Session
from app.utils.jwt_decode import get_id

router = APIRouter()

#Crear el mensaje base de una conversacion para un usuario autenticado
@router.get("/createbase", response_model=MessageIA)
def CreateBase(db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return create_base(db=db, user_id=user_id)

#Crear un nuevo mensaje en una conversacion para un usuario autenticado
@router.post("/create", response_model=List[MessageRead])
def Create(message: MessageCreate, db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return create(message=message, db=db, user_id=user_id)

#Obtener todos los mensajes de una conversacion para un usuario autenticado
@router.get("/getall/{conversation_id}", response_model=List[MessageRead])
def GetAll(conversation_id: int, db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return get_all(db=db, user_id=user_id, conversation_id=conversation_id)