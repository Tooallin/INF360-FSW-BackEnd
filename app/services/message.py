from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import conversation as CrudConversation
from app.crud import message as CrudMessage
from app.schemas.message import MessageCreate, MessageRead
from app.utils import ia

def create_base(db: Session, user_id: int, conversation_id: int):
	#Verificamos que la conversacion pertenezca al usuario
	conversation = CrudConversation.get_by_user_and_id(db, user_id, conversation_id)
	if not conversation:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"No se encontró la conversación {conversation_id} para el usuario {user_id}."
		)

	#Generamos un mensaje base para la conversación
	try:
		base_text = ia.generate_base()
	except ValueError as e:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(e)
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Error al generar mensaje base: {str(e)}"
		)
	
	#Una vez generado el mensaje correctamente lo incluimos en la conversacion en la BD
	base_msg = MessageCreate(
		conversation_id=conversation_id,
		sender=False,
		content=base_text
	)
	saved = CrudMessage.create(db, base_msg)

	return MessageRead.model_validate(saved).model_dump()

def create(message: MessageCreate, db: Session, user_id: int):
	#Verificamos que la conversacion pertenezca al usuario
	conversation = CrudConversation.get_by_user_and_id(db, user_id, message.conversation_id)
	if not conversation:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"La conversación {message.conversation_id} no existe o no pertenece al usuario {user_id}"
		)
	
	#Almacenamos el mensaje del usuario
	user_msg_in = MessageCreate(
		conversation_id=message.conversation_id,
		sender=True,
		content=message.content
	)
	user_msg = CrudMessage.create(db, user_msg_in)

	#Obtenemos una respuesta de la IA
	try:
		ia_content = ia.generate(message=message.content)
	except TimeoutError as e:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail=f"Se acabó el tiempo de respuesta de la IA: {str(e)}"
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Error al consultar IA: {str(e)}"
		)
	
	#Almacenamos la respuesta de la IA
	ia_msg_in = MessageCreate(
		conversation_id=message.conversation_id,
		sender=False,
		content=ia_content
	)
	ia_msg = CrudMessage.create(db, ia_msg_in) 
	CrudConversation.update_date(db, message.conversation_id)
	#Retornamos ambos mensajes
	return [user_msg, ia_msg]
	
def get_all(db: Session, user_id: int, conversation_id: int):
	#Verificamos que la conversacion pertenezca al usuario
	conversation = CrudConversation.get_by_user_and_id(db, user_id, conversation_id)
	if not conversation:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"La conversación {conversation_id} no existe o no pertenece al usuario {user_id}"
		)
	
	#Retornamos los mensajes de forma cronologica
	return CrudMessage.get_all(db, conversation_id)