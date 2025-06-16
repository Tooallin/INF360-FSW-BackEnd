from app.utils import ia
from app.schemas.message import MessageCreate, MessagePack, MessageOut
from app.crud import message as Crud
from sqlalchemy.orm import Session
from app.utils import translate
from fastapi import HTTPException, status

def create(message: MessageCreate, db: Session):
	#DE AQUI PARA ABAJO DEBERIA SER UN TRY-CATCH

	exception = HTTPException(
		status_code=status.HTTP_400_BAD_REQUEST,
		detail="Error al generar respuesta"
	)

	#CASO DE ERROR EN RESPUESTA DE DEEPSEEK
	try:
		ia_response = ia.generate(message=message.user_question)
		ia_response_spanish = translate.to_spanish(text=ia_response)
	except Exception as e:
		raise exception  # Vuelve a lanzar la excepción original

	'''
	response = MessageOut(
		id=1,
		id_chat=message.id_chat,
		user_question=message.user_question,
		ia_response=ia_response_spanish
	)
	'''

	# AQUI UN CASO DE ERROR EN LA BD
	# ADEMÁS HAY QUE MODIFICAR LO QUE ESPERA Crud.create()
	response = Crud.create(db, MessagePack(
		id_chat=message.id_chat,
		user_question=message.user_question,
		ai_response=ia_response_spanish
	))

	return response

def get_all(id_chat: int, db: Session):
	return Crud.get_all(db, id_chat)