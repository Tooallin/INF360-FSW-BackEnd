from app.utils import ia
from app.schemas.message import MessageCreate, MessagePack, MessageOut
from app.crud import message as Crud
from app.crud import chat as CrudChat
from sqlalchemy.orm import Session
from app.utils import translate
from fastapi import HTTPException, status

def create_base():
	try:
		ai_response = ia.generate_base()
		ai_response_spanish = translate.to_spanish(text=ai_response)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_406_NOT_ACCEPTABLE,
			detail=str(e)
		)

	response = MessageOut(
		id=-1,
		id_chat=-1,
		user_question="",
		#ai_response=ai_response
		ai_response=ai_response_spanish
	)

	return response

def create(message: MessageCreate, db: Session, id_user: int):
	# Alguien intentando añadir un mensaje de un chat que no es suyo
	chats = CrudChat.get_all(db, id_user)

	if chats.filter(chats.id_chat == message.id_chat) is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Ocurrió un error inesperado"
		)

	# Si intenta añadir a mensajes a un chat suyo se continua con el comportamiento esperado

	#DE AQUI PARA ABAJO DEBERIA SER UN TRY-CATCH

	exception = HTTPException(
		status_code=status.HTTP_400_BAD_REQUEST,
		detail="Error al generar respuesta"
	)

	#CASO DE ERROR EN RESPUESTA DE DEEPSEEK
	try:
		ai_response = ia.generate(message=message.user_question)
		ai_response_spanish = translate.to_spanish(text=ai_response)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_406_NOT_ACCEPTABLE,
			detail=str(e)
		)


	'''
	response = MessageOut(
		id=1,
		id_chat=-1,
		user_question=message.user_question,
		#ai_response=ai_response
		ai_response=ai_response_spanish
	)
	'''

	# AQUI UN CASO DE ERROR EN LA BD
	# ADEMÁS HAY QUE MODIFICAR LO QUE ESPERA Crud.create()}
	
	response = Crud.create(db, MessagePack(
		id_chat=message.id_chat,
		user_question=message.user_question,
		ai_response=ia_response_spanish
	))

	return response

def get_all(id_chat: int, db: Session, id_user: int):
	# Alguien intentando obtener mensajes de un chat que no es suyo
	chats = CrudChat.get_all(db, id_user)

	if chats.filter(chats.id_chat == id_chat) is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Ocurrió un error inesperado"
		)

	# Si intenta acceder a mensajes de un chat suyo se retorna lo correspondiente
	return Crud.get_all(db, id_chat)