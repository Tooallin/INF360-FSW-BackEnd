from pydantic import BaseModel

class MessageCreate(BaseModel):
	id_chat: int
	user_question: str
	ia_response: str
	
class MessageOut(MessageCreate):
	id: int