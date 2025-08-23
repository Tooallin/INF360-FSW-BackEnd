from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate

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

def get_clinical_history(db: Session, id: int):
    return db.query(User.name, User.surname, User.age, User.gender, User.profesion, User.hobbies).filter(User.id == id).first()

def get_hobbies(db: Session, id: int):
    return db.query(User.hobbies).filter(User.id == id).first()

def update_user(db: Session, user: UserUpdate, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    # Actualizar campos existentes
    if user.name:
        db_user.name = user.name

    db_user.surname = user.surname

    if user.email:
        db_user.email = user.email

    if user.password:
        db_user.password = user.password

    db_user.age = user.age
    db_user.gender = user.gender
    db_user.profesion = user.profesion
    db_user.hobbies = user.hobbies

    db.commit()
    db.refresh(db_user)
    return db_user
