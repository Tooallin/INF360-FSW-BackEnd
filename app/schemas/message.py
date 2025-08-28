from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer

class MessageCreate(BaseModel):
	model_config = ConfigDict(use_enum_values=True)
	role: str
	conversation_id: int
	content: str

	@field_validator("role")
	@classmethod
	def role_must_be_user_or_model(cls, v: str) -> str:
		if isinstance(v, str) and v.lower() in {"user", "model"}:
			return v.lower()
		raise ValueError("El campo role debe ser 'user' o 'model'")

class MessageRead(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	conversation_id: int
	role: str
	content: str
	created_at: datetime

class MessageIA(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	content: str

class MessageTranscribed(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	content: str