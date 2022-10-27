from typing import Optional
from pydantic import BaseModel,EmailStr,conint
from datetime import datetime


class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime
    class Config:
        orm_mode = True

# Defining a schema for createposts
class BasePost(BaseModel):
    title:str
    content:str
    published: bool = True
    owner : UserOut

class PostCreate(BasePost):
    pass

class Post(BasePost):
    id:int
    created_at:datetime
    owner_id : int
    class Config:
        orm_mode = True
class PostOut(BaseModel):
    Post:Post
    votes : int

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir : conint(le = 1)