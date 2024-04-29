# from app.api.handlers.auth_handlers import UserHandler
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.utils.token import verify_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


# def get_current_user(token: str = Depends(verify_token)):
#     # Logic to get current user from token
#     pass


from fastapi import Depends, HTTPException
from app.utils.token import verify_token

async def get_current_user(token_data: dict = Depends(verify_token)):
    """
    Dependency function to get the current logged-in user based on the provided authentication token.
    """
    if token_data is None:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    if "sub" not in token_data:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user_id = token_data["sub"]
    return {"user_id": user_id}


def get_from_cache(key):
    # Logic to retrieve data from cache
    pass


def add_to_cache(key, value):
    # Logic to add data to cache
    pass
