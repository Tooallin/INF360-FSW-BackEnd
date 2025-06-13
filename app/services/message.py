from app.services import translate, ia
from app.schemas.message import MessageCreate, MessageOut
from app.crud import message as Crud
from sqlalchemy.orm import Session

def create(message: MessageCreate, db: Session):
	#DE AQUI PARA ABAJO DEBERIA SER UN TRY-CATCH

	#CASO DE ERROR EN RESPUESTA DE DEEPSEEK
	ia_response = ia.generate(message=message.user_question)

	response = MessageOut(
		id=1,
		id_chat=message.id_chat,
		user_question=message.user_question,
		ia_response=translate.to_spanish(text=ia_response)
	)

	# AQUI UN CASO DE ERROR EN LA BD
	# ADEMÁS HAY QUE MODIFICAR LO QUE ESPERA Crud.create()
	# Crud.create(db, message)

	return response

def get_all(id_chat: int, db: Session):
	return Crud.get_all(db, id_chat)