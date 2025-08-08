from app.db.models.conversation import Conversation
from sqlalchemy.orm import Session

def create(db: Session, user_id: int) -> Conversation:
	db_Conversation = Conversation(user_id=user_id)
	db.add(db_Conversation)
	db.commit()
	db.refresh(db_Conversation)
	return db_Conversation

def get_all(db: Session, user_id: int):
	return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def get_chat_by_user_and_id(db: Session, user_id: int, conversation_id: int):
    return db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.id == conversation_id
    ).first()