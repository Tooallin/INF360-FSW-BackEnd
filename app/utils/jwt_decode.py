from fastapi import HTTPException, status
from jose import jwt, JWTError
import os

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