from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_id(jwt_token: str = Depends(oauth2)):
	exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Credenciales de autenticación inválidas",
		headers={"WWW-Authenticate": "Bearer"})
	
	try:
		id = jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]).get("sub")
		if id is None:
			raise exception

	except JWTError as e:
		print(f"JWT error: {e}")
		raise exception

	return int(id)