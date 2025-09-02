from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
	init_db()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_origin_regex=r"https://.*\.ngrok-free\.app",
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.include_router(api_router, prefix="/api")