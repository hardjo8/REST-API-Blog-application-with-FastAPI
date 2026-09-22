
from pydantic import BaseModel,EmailStr
from datetime import datetime




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Config:
    orm_mode=True

class PostRespone(PostBase):
    created_at : datetime
    id:int

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class CreatedUser(BaseModel):
    email: EmailStr
    id:int
    created_at:datetime