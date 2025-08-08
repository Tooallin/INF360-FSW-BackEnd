from app.crud import conversation as Crud
from app.schemas.conversation import ConversationCreate
from sqlalchemy.orm import Session

def create(db: Session, user_id: int):
	return Crud.create(db, user_id)

def get_all(db: Session, user_id: int):
	return Crud.get_all(db, user_id)