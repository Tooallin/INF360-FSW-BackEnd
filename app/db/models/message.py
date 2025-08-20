from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, BigInteger
from sqlalchemy.sql import func

from app.db.base import Base

class Message(Base):
	__tablename__ = "messages"

	id = Column(Integer, primary_key=True, index=True)
	conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
	role = Column(Text, nullable=False)
	content = Column(Text, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)