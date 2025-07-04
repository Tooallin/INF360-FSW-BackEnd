from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserLogin

def create(db: Session, user: UserCreate) -> User:
	db_user = User(
		name=user.name,
		surname=user.surname,
		email=user.email,
		password=user.password,
		age=user.age,
		gender=user.gender
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def get_all(db: Session):
	return db.query(User).all()

def search_user_password(db: Session, user: UserLogin):
    return db.query(User).filter(User.email == user.email).first()
