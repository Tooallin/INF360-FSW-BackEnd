from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from app.db.session import engine

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	surname = Column(String, nullable=False)
	email = Column(String, unique=False, index=True)
	password = Column(String, nullable=False)
	age = Column(Integer, nullable=True)
	gender = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)