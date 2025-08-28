from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File
from app.api import deps
from app.schemas.message import MessageCreate, MessageRead, MessageIA, MessageTranscribed
from app.services.message import create, create_base, get_all, transcribe
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
def Create(message: MessageCreate, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return create(message=message, db=db, user_id=user_id, background_tasks=background_tasks)

#Obtener todos los mensajes de una conversacion para un usuario autenticado
@router.get("/getall/{conversation_id}", response_model=List[MessageRead])
def GetAll(conversation_id: int, db: Session = Depends(deps.get_db), user_id: int = Depends(get_id)):
	return get_all(db=db, user_id=user_id, conversation_id=conversation_id)

#Transcribir mensaje (Recibe voz, retorna texto)
@router.post("/transcribe", response_model=MessageTranscribed)
async def Transcribe(audio: UploadFile = File(...), user_id: int = Depends(get_id)):
	return await transcribe(audio=audio)