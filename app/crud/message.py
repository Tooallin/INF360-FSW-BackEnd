from sqlalchemy.orm import Session

from app.db.models.message import Message
from app.schemas.message import MessageCreate

def create(db: Session, message: MessageCreate) -> Message:
	db_Message = Message(
		conversation_id=message.conversation_id,
		sender=message.sender.value if hasattr(message.sender, "value") else message.sender,
		content=message.content
	)
	db.add(db_Message)
	db.commit()
	db.refresh(db_Message)
	return db_Message

def get_conversation(db: Session, conversation_id: int):
	return db.query(Message).filter(Message.conversation_id == conversation_id).all()