from app.schemas.message import MessageCreate
from app.db.session import SessionLocal
from app.crud import message as Crud

def create(message: MessageCreate):
	db = SessionLocal()
	try:
		return Crud.create(db, message)
	finally:
		db.close()

def get_all(id_chat: int):
	db = SessionLocal()
	try:
		return Crud.get_all(db, id_chat)
	finally:
		db.close()