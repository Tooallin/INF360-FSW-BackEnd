from app.schemas.chat import ChatCreate
from app.db.session import SessionLocal
from app.crud import chat as Crud

def create(chat: ChatCreate):
	db = SessionLocal()
	try:
		return Crud.create(db, chat)
	finally:
		db.close()

def get_all():
	db = SessionLocal()
	try:
		return Crud.get_all(db)
	finally:
		db.close()