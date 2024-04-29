from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    test: str


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    ack: str
    token: str
    token_type: str