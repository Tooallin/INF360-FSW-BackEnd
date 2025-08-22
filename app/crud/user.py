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
		gender=user.gender,
		profesion=user.profesion,
		hobbies=user.hobbies
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def get_all(db: Session):
	return db.query(User).all()

def search_user_password(db: Session, user: UserLogin):
    return db.query(User).filter(User.email == user.email).first()

def get_medical_record(db: Session, id: int):
    return db.query(User.name, User.surname, User.age, User.gender, User.profesion, User.hobbies).filter(User.id == id).first()

def get_hobbies(db: Session, id: int):
    return db.query(User.hobbies).filter(User.id == id).first()

def update_user(db: Session, user: UserCreate, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    # Actualizar campos existentes
    db_user.name = user_data.name
    db_user.surname = user_data.surname
    db_user.email = user_data.email
    db_user.password = user_data.password
    db_user.age = user_data.age
    db_user.gender = user_data.gender
    db_user.profesion = user_data.profesion
    db_user.hobbies = user_data.hobbies

    db.commit()
    db.refresh(db_user)
    return db_user
