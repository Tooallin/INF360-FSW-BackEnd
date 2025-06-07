from fastapi import FastAPI
from pydantic import BaseModel
from schemas.user import User

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello World"}