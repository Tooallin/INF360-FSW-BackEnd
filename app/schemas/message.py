import enum
from datetime import datetime
from pydantic import BaseModel

class SenderType(enum.Enum):
	user = "user"
	ai = "ai"

class MessageCreate(BaseModel):
	conversation_id: int
	sender: SenderType
	content: str
	
class MessageOut(MessageCreate):
	id: int
	conversation_id: int
	sender: SenderType
	content: str
	created_at: datetime