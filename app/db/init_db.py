from app.db.base import Base
from app.db.session import engine

def import_models() -> None:
	import pkgutil, importlib, app.db.models as models_pkg
	for finder, name, ispkg in pkgutil.iter_modules(models_pkg.__path__):
		importlib.import_module(f"{models_pkg.__name__}.{name}")

def init_db():
	with engine.begin() as conn:
		conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector;")
	import_models()
	Base.metadata.create_all(bind=engine)