import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	postgres_user: str
	postgres_password: str
	postgres_db: str
	postgres_host: str
	postgres_port: str

	deepseek_host: str
	deepseek_port: str

	jwt_algorithm: str
	jwt_secret: str

	model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
settings.deepseek_url = f"http://{settings.deepseek_host}:{settings.deepseek_port}/api/generate"

if os.getenv("PYTHONDONTWRITEBYTECODE") == "1":
	import sys
	sys.dont_write_bytecode = True