from fastapi import APIRouter
from typing import List, Dict
from app.schemas.user import UserCreate
from app.test.test import run_all_test

router = APIRouter()

@router.post("/run-tests")
def run_test(user: UserCreate):
    context: List[Dict] = []
    return run_all_test(user, context)