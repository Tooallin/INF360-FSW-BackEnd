from app.db.base import Base
from app.db.session import engine
from sqlalchemy import Column, Integer, DateTime, ForeignKey

class Conversation(Base):
	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), index=True)
	started_at = Column(DateTime, nullable=False)

Base.metadata.create_all(bind=engine)