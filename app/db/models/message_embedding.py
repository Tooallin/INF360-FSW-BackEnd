from sqlalchemy import Column, Integer, ForeignKey
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.core.config import settings

class MessageEmbedding(Base):
	__tablename__ = "message_embedding"

	message_id = Column(Integer, ForeignKey("message.id", ondelete="CASCADE"), primary_key=True)
	embedding = Column(Vector(settings.embedding_dimension), nullable=True)