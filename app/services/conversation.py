from sqlalchemy.orm import Session

from app.crud import conversation as Crud
from app.schemas.conversation import ConversationCreate

def create(conversation: ConversationCreate, db: Session, user_id: int):
	new_conversation = Crud.create(db, user_id)
	
	#Almacenamos el saludo de la IA
	ia_msg_in = MessageCreate(
		conversation_id=new_conversation.id,
		sender=False,
		content=conversation.ia_msg_in
	)
	ia_msg = CrudMessage.create(db, ia_msg_in) 

	CrudConversation.update_date(db, new_conversation.id)

	return new_conversation

def get_all(db: Session, user_id: int):
	return Crud.get_all(db, user_id)