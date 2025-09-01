from fastapi import HTTPException, status, BackgroundTasks, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.crud import conversation as CrudConversation
from app.crud import message as CrudMessage
from app.crud import user as CrudUser
from app.crud import message_embedding as CrudMessageEmbedding

from app.schemas.message import MessageCreate, MessageRead, MessageIA, MessageTranscribed
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.message_embedding import MessageEmbeddingCreate, MessageEmbeddingGet

from app.utils import transcribe as transcribe_utils
from app.utils import ia

def create_base(db: Session, user_id: int):
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

	return MessageIA(content=base_text)

def create(message: MessageCreate, db: Session, user_id: int, background_tasks: BackgroundTasks):
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
		role="user",
		content=message.content
	)
	user_msg = CrudMessage.create(db, user_msg_in)
	CrudMessageEmbedding.create(db, MessageEmbeddingCreate(message_id=user_msg.id, embedding=ia.embed_message(user_msg.content)))

	#Procesar y actualizar historial clinico
	background_tasks.add_task(update_and_process_clinical_history, message, user_id)

	#Obtenemos una respuesta de la IA
	try:
		memory_size = 10
		ia_content = ia.generate(message=message.content, context=generate_context(db, memory_size, message), user_record=ia.format_clinical_history(CrudUser.get_clinical_history(db, user_id)))
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
		role="model",
		content=ia_content
	)
	ia_msg = CrudMessage.create(db, ia_msg_in) 
	CrudMessageEmbedding.create(db, MessageEmbeddingCreate(message_id=ia_msg.id, embedding=ia.embed_message(ia_msg.content)))

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

def generate_context(db: Session, k: int, user_msg_in: MessageCreate):
	last_k = CrudMessage.get_last_k(db, user_msg_in.conversation_id, k)
	similar_k = CrudMessageEmbedding.get_similar(db, MessageEmbeddingGet(
		conversation_id=user_msg_in.conversation_id,
		embedding=ia.embed_message(user_msg_in.content),
		k=k
	))
	return ia.build_history(last_k, similar_k)

def update_and_process_clinical_history(message: MessageCreate, user_id: int):
	db = SessionLocal()
	#Actualizar historial clinico
	try:
		old_hobbies = CrudUser.get_hobbies(db, user_id)
		clinical_history = ia.new_clinical_history(message=message.content, hobbies_string=ia.format_clinical_history(old_hobbies))
		print(clinical_history)
		CrudUser.update_user(db, UserUpdate(
			name=clinical_history["name"],
			surname=clinical_history["surname"],
			age=clinical_history["age"],
			gender=clinical_history["gender"],
			profesion=clinical_history["profesion"],
			hobbies=clinical_history["hobbies"]
		), user_id)
		db.commit()
	except TimeoutError as e:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail=f"Se acabó el tiempo de respuesta de la IA: {str(e)}"
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Error al actualizar historial clínico: {str(e)}"
		)
	finally:
		db.close()

async def transcribe_message(audio: UploadFile) -> MessageTranscribed:
	texto = await transcribe_utils.transcribe(audio)
	return MessageTranscribed(
		content=texto
	)