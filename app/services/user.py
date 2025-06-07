from app.schemas.user import UserCreate
from app.db.session import SessionLocal
from app.crud import user as Crud

def create(user: UserCreate):
	db = SessionLocal()
	try:
		return Crud.create(db, user)
	finally:
		db.close()

def get_all():
	db = SessionLocal()
	try:
		return Crud.get_all(db)
	finally:
		db.close()