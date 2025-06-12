from app.schemas.user import UserCreate
from app.crud import user as Crud
from sqlalchemy.orm import Session

def create(user: UserCreate, db: Session):
	return Crud.create(db, user)

def get_all(db: Session):
	return Crud.get_all(db)