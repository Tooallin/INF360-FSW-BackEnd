from typing import List
from pydantic import BaseModel, field_validator, field_serializer

from app.core.config import settings

class MessageEmbeddingCreate(BaseModel):
	message_id: int
	embedding: List[float]

	@field_validator("embedding")
	@classmethod
	def check_length(cls, v):
		if len(v) != settings.embedding_dimension:
			raise ValueError(f"El embedding debe tener {settings.embedding_dimension} dimensiones")
		return v

	@field_serializer("embedding")
	def serialize_embedding(self, v):
		return list(v)

class MessageEmbeddingGetKSimilar(BaseModel):
	conversation_id: int
	embedding: List[float]
	k: int

	@field_validator("embedding")
	@classmethod
	def check_length(cls, v):
		if len(v) != settings.embedding_dimension:
			raise ValueError(f"El embedding debe tener {settings.embedding_dimension} dimensiones")
		return v

	@field_serializer("embedding")
	def serialize_embedding(self, v):
		return list(v)