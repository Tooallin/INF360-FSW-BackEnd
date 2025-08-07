from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.user import UserCreate, UserOut, UserLogin, UserJWT
from app.services.user import create, get_all, login
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", response_model=UserOut)
def Create(user: UserCreate, db: Session = Depends(deps.get_db)):
	return create(user=user, db=db)

@router.get("/getall", response_model=List[UserOut])
def GetAll(db: Session = Depends(deps.get_db)):
	return get_all(db=db)

@router.post("/login", response_model=UserJWT)
def Login(user: UserLogin, db: Session = Depends(deps.get_db)):
	return login(user=user, db=db)