from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from app.db.session import engine

class Message(Base):
	__tablename__ = "message"

	id = Column(Integer, primary_key=True, index=True)
	id_chat = Column(Integer, ForeignKey("chat.id"), index=True)
	user_question = Column(String, nullable=False)
	ai_response = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)