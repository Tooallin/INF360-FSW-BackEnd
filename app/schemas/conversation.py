from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ConversationCreate(BaseModel):
	pass
	
class ConversationOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	user_id: int
	started_at: datetime