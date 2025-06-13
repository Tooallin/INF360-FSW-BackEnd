from pydantic import BaseModel

class UserCreate(BaseModel):
	name: str
	surname: str
	email: str
	password: str
	age: int
	gender: str

class UserOut(UserCreate):
	id: int

class UserLogin(BaseModel):
	email: str
	password: str

class UserJWT(BaseModel):
	access_token: str
	token_type: str