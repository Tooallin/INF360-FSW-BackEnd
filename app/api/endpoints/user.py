from fastapi import APIRouter
from app.schemas.user import UserCreate, UserOut
from app.services.user import create, get_all
from typing import List

router = APIRouter()

@router.post("/create", response_model=UserOut)
def Create(user: UserCreate):
	return create(user=user)

@router.get("/getall", response_model=List[UserOut])
def GetAll():
	return get_all()