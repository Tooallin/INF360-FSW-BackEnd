from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
	name: str
	surname: str
	url: str
	age: int

@app.get("/")
async def root():
	return {"message": "Hello World"}

#Documentacion https://127.0.0.1/docs
#Documentacion https://127.0.0.1/redoc

#Levantar server: uvicorn main:app --reload