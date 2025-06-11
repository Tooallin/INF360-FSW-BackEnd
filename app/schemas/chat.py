from pydantic import BaseModel

class ChatCreate(BaseModel):
	id_user: int
	counter: int
	
class ChatOut(ChatCreate):
	id: int