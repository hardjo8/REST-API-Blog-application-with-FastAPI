
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Config:
    orm_mode=True

class PostResponse(PostBase):
    created_at : datetime
    id:int
    user_id : int

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class CreatedUser(BaseModel):
    email: EmailStr
    id:int
    created_at:datetime

class UserLogin(BaseModel):
    email : EmailStr
    password :str

class Config:
    orm_mode=True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None
    