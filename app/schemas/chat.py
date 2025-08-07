from pydantic import BaseModel

class ChatCreate(BaseModel):
	counter: int
	
class ChatOut(ChatCreate):
	id: int