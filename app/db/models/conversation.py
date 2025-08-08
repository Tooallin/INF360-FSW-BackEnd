from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.db.base import Base

class Conversation(Base):
	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
	started_at = Column(DateTime, nullable=False)