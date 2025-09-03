from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ConversationCreate(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	ia_msg_in: str
	
class ConversationOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	user_id: int
	title: Optional[str] = None
	updated_at: datetime