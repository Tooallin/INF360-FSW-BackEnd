from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base

class Conversation(Base):
	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
	title = Column(String(120), index=True, nullable=True)
	updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        #onupdate=func.now(),🔹 Esto actualiza el campo en UPDATE
        nullable=False
    )