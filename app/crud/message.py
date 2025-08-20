from sqlalchemy.orm import Session

from app.db.models.message import Message
from app.schemas.message import MessageCreate

def create(db: Session, message: MessageCreate) -> Message:
	db_Message = Message(
		conversation_id=message.conversation_id,
		role=message.role,
		content=message.content
	)
	db.add(db_Message)
	db.commit()
	db.refresh(db_Message)
	return db_Message

def get_conversation(db: Session, conversation_id: int):
	return db.query(Message).filter(Message.conversation_id == conversation_id).all()

def get_last_k(db: Session, conversation_id: int, k: int):
	db_Messages = (
		db.query(Message)
		.filter(Message.conversation_id == conversation_id)
		.order_by(Message.created_at.des(), Message.id.asc())
		.limit(k)
	)
	return db_Messages

def get_all(db: Session, conversation_id: int):
	db_Messages = (
		db.query(Message)
		.filter(Message.conversation_id == conversation_id)
		.order_by(Message.created_at.asc(), Message.id.asc())
		.all()
	)
	return db_Messages