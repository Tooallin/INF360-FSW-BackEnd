from sqlalchemy.orm import Session

from app.crud import conversation as CrudConversation
from app.crud import message as CrudMessage
from app.crud import message_embedding as CrudMessageEmbedding
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate
from app.schemas.message_embedding import MessageEmbeddingCreate

from app.utils import ia

def create(conversation: ConversationCreate, db: Session, user_id: int):
	new_conversation = CrudConversation.create(db, user_id)
	
	#Almacenamos el saludo de la IA
	ia_msg_in = MessageCreate(
		conversation_id=new_conversation.id,
		role="model",
		content=conversation.ia_msg_in
	)
	ia_msg = CrudMessage.create(db, ia_msg_in)
	CrudMessageEmbedding.create(db, MessageEmbeddingCreate(message_id=ia_msg.id, embedding=ia.embed_message(ia_msg.content)))

	CrudConversation.update_date(db, new_conversation.id)

	return new_conversation

def get_all(db: Session, user_id: int):
	return CrudConversation.get_all(db, user_id)