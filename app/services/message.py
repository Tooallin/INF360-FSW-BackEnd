from app.schemas.message import MessageCreate
from app.crud import message as Crud
from sqlalchemy.orm import Session

def create(message: MessageCreate, db: Session):
	return Crud.create(db, message)

def get_all(id_chat: int, db: Session):
	return Crud.get_all(db, id_chat)