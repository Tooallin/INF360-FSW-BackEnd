from sqlalchemy.orm import Session
from app.db.models.chat import Chat
from app.schemas.chat import ChatCreate

def create(db: Session, chat: ChatCreate, id_user: int) -> Chat:
	db_chat = Chat(
		id_user=id_user,
		counter=chat.counter
	)
	db.add(db_chat)
	db.commit()
	db.refresh(db_chat)
	return db_chat

def get_all(db: Session, id_user: int):
	return db.query(Chat).filter(Chat.id_user == id_user).all()