from app.schemas.chat import ChatCreate
from app.crud import chat as Crud
from sqlalchemy.orm import Session

def create(chat: ChatCreate, db: Session, id_user: int):
	return Crud.create(db, chat, id_user)

def get_all(db: Session, id_user: int):
	return Crud.get_all(db, id_user)