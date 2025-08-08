from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

class MessageCreate(BaseModel):
	model_config = ConfigDict(use_enum_values=True)
	conversation_id: int
	content: str

class MessageRead(BaseModel):
	id: int
	conversation_id: int
	sender: Literal["user", "ia"]
	content: str
	created_at: datetime