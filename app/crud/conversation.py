from app.db.models.conversation import Conversation
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

def create(db: Session, user_id: int) -> Conversation:
	db_Conversation = Conversation(user_id=user_id)
	db.add(db_Conversation)
	db.commit()
	db.refresh(db_Conversation)
	return db_Conversation

def get_all(db: Session, user_id: int):
	return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()

def get_by_user_and_id(db: Session, user_id: int, conversation_id: int):
	return db.query(Conversation).filter_by(
		user_id=user_id,
		id=conversation_id
	).first()

def update_date(db: Session, conversation_id: int):
    db.query(Conversation).filter(Conversation.id == conversation_id).update(
        {Conversation.updated_at: func.now()}
    )
    db.commit()