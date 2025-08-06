from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings


def get_id(jwt_token: str):
	exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Credenciales de autenticación inválidas",
		headers={"WWW-Authenticate": "Bearer"})
	
	try:
		id = jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]).get("sub")
		if id is None:
			raise exception

	except JWTError:
		raise exception

	return id