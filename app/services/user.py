from app.schemas.user import UserCreate, UserJWT, UserLogin
from app.crud import user as Crud
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv
load_dotenv()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


def create(user: UserCreate, db: Session):
	user.password = crypt.hash(user.password)
	return Crud.create(db, user)

def get_all(db: Session):
	return Crud.get_all(db)

def login(user: UserLogin, db: Session):
	id = auth_user_by_credentials(user, db)
	expire =  datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_DURATION")))

	access_token = {"sub": id, "exp": expire}
	return UserJWT(access_token=jwt.encode(access_token, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM")),token_type="bearer")

def auth_user_by_credentials(user: UserLogin, db: Session):
	exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Credenciales de autenticación inválidas",
		headers={"WWW-Authenticate": "Bearer"})
	
	user_get = Crud.search_user_password(db, user)
	if user_get is None or not crypt.verify(user.password,user_get.password):
		raise exception
	
	return user_get.id

def get_id(jwt_token: str):
	exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Credenciales de autenticación inválidas",
		headers={"WWW-Authenticate": "Bearer"})
	
	try:
		username = jwt.decode(jwt_token, os.getenv("SECRET"), algorithms=[os.getenv("ALGORITHM")]).get("sub")
		if username is None:
			raise exception

	except JWTError:
		raise exception

	return username

'''
#Función pendiente por implementar
async def auth_user_by_jwt(user: UserLogin, db: Session):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        user_get = Crud.search_user_password(db, user)
        if user_get is None or not crypt.verify(user.password,user_get.password):
            raise exception
        
        username = jwt.decode(token, os.getenv("SECRET"), algorithms=[os.getenv("ALGORITHM")]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return None
'''