from sqlalchemy.orm import Session
from app.db.models.message import Message
from app.schemas.message import MessageCreate

def create(db: Session, message: MessageCreate) -> Message:
	db_Message = Message(
		id_chat=message.id_chat,
		user_question=message.user_question,
		ai_response=message.ai_response
	)
	db.add(db_Message)
	db.commit()
	db.refresh(db_Message)
	return db_Message

def get_all(db: Session, id_chat: int):
	return db.query(Message).filter(Message.id_chat == id_chat).all()