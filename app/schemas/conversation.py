from datetime import datetime
from pydantic import BaseModel

class ConversationCreate(BaseModel):
	pass
	
class ConversationOut():
	id: int
	user_id: int
	started_at: datetime

	model_config = {"from_attributes": True}