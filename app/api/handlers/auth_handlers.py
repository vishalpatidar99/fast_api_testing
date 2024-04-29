from app.schemas.models import User
from fastapi import (
    HTTPException, 
    status
)
from app.utils.auth import get_password_hash, verify_password
from app.utils.token import cache, create_access_token
from app.schemas.schemas import UserResponse
from sqlalchemy.exc import SQLAlchemyError


class UserHandler:

    def signup(self, user, db):
        try:
            # Hash password
            hashed_password = get_password_hash(user.password)
            new_user = User(email=user.email, password=hashed_password)
        
            existing_user = db.query(User).filter(User.email == new_user.email).first()
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

            # Create user in database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            access_token = create_access_token(data={"sub": User.email})
            return UserResponse(ack="User created successfully", token=access_token, token_type="bearer")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occurred while creating the user")

    def login(self, user, db):
        try:
            user_db = db.query(User).filter(User.email == user.email).first()
            if not user_db:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

            # Verify password
            if not verify_password(user.password, user_db.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
            access_token = create_access_token(data={"sub": user.email})
            return UserResponse(ack="User Logged in successfully", token=access_token, token_type="bearer")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occurred while logging in the user")