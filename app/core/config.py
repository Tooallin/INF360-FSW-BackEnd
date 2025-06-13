import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	postgres_user: str
	postgres_password: str
	postgres_db: str
	postgres_host: str = "localhost"
	postgres_port: str = "5432"

	deepseek_host: str = "localhost"
	deepseek_port: str = "11434"

	deepseek_url: str = f"{deepseek_host}:{deepseek_port}/api/generate"

	model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()

if os.getenv("PYTHONDONTWRITEBYTECODE") == "1":
	import sys
	sys.dont_write_bytecode = True