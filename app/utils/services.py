from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models import User
from cachetools import TTLCache
from datetime import datetime, timedelta, timezone
from app.constants import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes cache

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create JWT access token with the provided data.
    :param data: Data to include in the token payload
    :param expires_delta: Optional expiration time delta
    :return: Generated JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Default expiration time

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    # Logic to verify token
    pass


def get_current_user(token: str = Depends(verify_token)):
    # Logic to get current user from token
    pass


def get_from_cache(key):
    # Logic to retrieve data from cache
    pass


def add_to_cache(key, value):
    # Logic to add data to cache
    pass
