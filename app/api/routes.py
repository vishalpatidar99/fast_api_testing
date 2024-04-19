from fastapi import (
    APIRouter,
    Depends, 
    HTTPException, 
    status
)
from app.utils.services import cache, create_access_token
from app.schemas.models import User
from app.schemas.schemas import PostCreate, Post
from app.schemas.schemas import UserCreate
from app.utils.services import get_current_user
from app.utils.utils import get_password_hash, verify_password
from app.db.db import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup/", response_model=dict)
async def signup(user: UserCreate, db: Session = Depends(SessionLocal)):
    existing_user = User.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password
    hashed_password = get_password_hash(user.password)

    # Create user in database
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": User.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/", response_model=dict)
async def login(user: UserCreate):
    user_db = User.get_user_by_email(user.email)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    # Verify password
    if not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/getposts/", response_model=list[Post])
async def get_posts(current_user: User = Depends(get_current_user)):
    # Logic for retrieving user's posts (fetch from DB, apply caching, etc.)
    pass


@router.post("/addpost/", response_model=Post)
async def add_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    # Logic for adding a post (validate payload, save post in DB, etc.)
    pass


@router.delete("/deletepost/{post_id}/")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    # Logic for deleting a post (verify ownership, delete from DB, etc.)
    pass
