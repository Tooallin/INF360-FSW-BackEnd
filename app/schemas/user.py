from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
	name: str
	surname: Optional[str] = None  # Opcional
	email: str
	password: str
	age: Optional[int] = None      # Opcional
	gender: Optional[str] = None   # Opcional
	profesion: Optional[str] = None      # Opcional
	hobbies: Optional[List[str]] = None   # Opcional

class UserOut(UserCreate):
	id: int

class UserLogin(BaseModel):
	email: str
	password: str

class UserJWT(BaseModel):
	access_token: str
	token_type: str