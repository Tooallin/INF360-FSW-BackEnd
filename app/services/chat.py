from app.schemas.chat import ChatCreate
from app.crud import chat as Crud
from sqlalchemy.orm import Session

def create(chat: ChatCreate, db: Session):
	return Crud.create(db, chat)

def get_all(db: Session):
	return Crud.get_all(db)