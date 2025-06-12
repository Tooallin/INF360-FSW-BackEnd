import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	postgres_user: str
	postgres_password: str
	postgres_db: str
	postgres_host: str = "localhost"
	postgres_port: str = "5432"

	model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()

if os.getenv("PYTHONDONTWRITEBYTECODE") == "1":
	import sys
	sys.dont_write_bytecode = True