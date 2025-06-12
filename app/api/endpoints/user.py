from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.user import UserCreate, UserOut
from app.services.user import create, get_all
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", response_model=UserOut)
def Create(user: UserCreate, db: Session = Depends(deps.get_db)):
	return create(user=user, db=Session)

@router.get("/getall", response_model=List[UserOut])
def GetAll(db: Session = Depends(deps.get_db)):
	return get_all(db=Session)