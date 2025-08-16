from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer

class MessageCreate(BaseModel):
	model_config = ConfigDict(use_enum_values=True)
	sender: int
	conversation_id: int
	content: str

	#Parsear a 1 o 0 siempre
	@field_validator("sender")
	@classmethod
	def sender_must_be_0_or_1(cls, v: int) -> int:
		if isinstance(v, bool):
			return 1 if v else 0
		if v in (0, 1):
			return v
		raise ValueError("El campo sender debe ser 0 (IA) o 1 (user)")

class MessageRead(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	conversation_id: int
	sender: bool
	content: str
	created_at: datetime

	#Parsear a 1 o 0 siempre
	@field_serializer("sender")
	def serialize_sender(self, v: bool) -> int:
		return 1 if v else 0

class MessageIA(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	content: str