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