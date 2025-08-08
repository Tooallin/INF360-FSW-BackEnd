import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.session import engine

class SenderType(enum.Enum):
	USER = "user"
	IA = "ia"

class Message(Base):
	__tablename__ = "messages"

	id = Column(Integer, primary_key=True, index=True)
	conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
	sender = Column(Enum(SenderType, name='sender_enum', validate_strings=True), nullable=False)
	content = Column(Text, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

Base.metadata.create_all(bind=engine)