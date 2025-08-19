from app.db.base import Base
from app.db.session import engine

def init_db():
	with engine.begin() as conn:
		conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector;")
	Base.metadata.create_all(bind=engine)