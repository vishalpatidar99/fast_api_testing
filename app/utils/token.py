from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm.attributes import InstrumentedAttribute
from cachetools import TTLCache
from datetime import datetime, timedelta, timezone
from app.utils.constants import SECRET_KEY, ALGORITHM
from jose.exceptions import ExpiredSignatureError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes cache


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create JWT access token with the provided data.
    :param data: Data to include in the token payload
    :param expires_delta: Optional expiration time delta
    :return: Generated JWT token
    """
    to_encode = {}
    for key, value in data.items():
        # Convert ORM attributes to JSON-serializable values
        if isinstance(value, InstrumentedAttribute):
            # Example: Convert ORM attribute to its value
            to_encode[key] = getattr(value, 'value', None)
        else:
            to_encode[key] = value

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Default expiration time

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str = Depends(oauth2_scheme)):
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get('user_id')  # Try getting user_id first
        # print(payload)
        
        if user is None:
            user = payload.get('sub')  # Try getting user_id from 'sub'
        
        # If user_id is still missing, raise HTTPException
        if user is None:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        
        return payload
    
    except ExpiredSignatureError:
        # If token has expired, raise HTTPException
        raise HTTPException(status_code=401, detail="Token Expired")
    
    except Exception as e:
        # If any other error occurs during token decoding, raise HTTPException
        raise HTTPException(status_code=500, detail="invalid or missing token ")

