from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.conversation import ConversationCreate, ConversationOut
from app.services.conversation import create, get_all
from typing import List
from sqlalchemy.orm import Session
from app.utils.jwt_decode import get_id

router = APIRouter()

#Crear una nueva conversacion para un usuario autenticado
@router.post("/create", response_model=ConversationOut)
def Create(db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return create(db=db, user_id=user_id)

#Obtener todas las conversaciones de un usuario autenticado
@router.get("/getall", response_model=List[ConversationOut])
def GetAll(db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return get_all(db=db, user_id=user_id)