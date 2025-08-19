import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	#PostgreSQL Environment
	postgres_user: str
	postgres_password: str
	postgres_db: str
	postgres_host: str
	postgres_port: str

	#DeepSeek Environment
	deepseek_host: str
	deepseek_port: str

	#JWT Environment
	jwt_algorithm: str
	jwt_secret: str
	access_token_duration: str

	#Gemini Environment
	gemini_api_key: str
	gemini_model: str
	embedding_model: str
	embedding_dimension: int

	model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
settings.deepseek_url = f"http://{settings.deepseek_host}:{settings.deepseek_port}/api/generate"

if os.getenv("PYTHONDONTWRITEBYTECODE") == "1":
	import sys
	sys.dont_write_bytecode = True