from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from app.db.session import engine

class Chat(Base):
	__tablename__ = "chat"

	id = Column(Integer, primary_key=True, index=True)
	id_user = Column(Integer, ForeignKey("users.id"), index=True)
	counter = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)