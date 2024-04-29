from fastapi import (
    APIRouter,
    Depends, 
    status
)
from app.schemas.schemas import UserCreate, UserResponse
from app.api.handlers.wrapper import get_user_handler
from app.db.db import get_db
from sqlalchemy.orm import Session

auth_router = APIRouter()

@auth_router.post("/signup/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_handler = get_user_handler()
    return user_handler.signup(user, db)
    

@auth_router.post("/login/", response_model=UserResponse)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    user_handler = get_user_handler()
    return user_handler.login(user, db)

