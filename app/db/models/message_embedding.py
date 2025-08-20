from sqlalchemy import Column, Integer, ForeignKey
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.core.config import settings

class MessageEmbedding(Base):
	__tablename__ = "message_embeddings"

	message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True)
	embedding = Column(Vector(settings.embedding_dimension), nullable=True)