from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.base import Base

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	surname = Column(String, nullable=True)
	email = Column(String, unique=True, index=True, nullable=False)
	password = Column(String, nullable=False)
	age = Column(Integer, nullable=True)
	gender = Column(String, nullable=True)
	profesion = Column(String, nullable=True)
	hobbies = Column(ARRAY(String), nullable=True)