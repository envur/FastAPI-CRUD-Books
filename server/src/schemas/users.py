from pydantic import BaseModel
from typing import List, Optional
from src.schemas.books import *

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True

class AllUsers(BaseModel):
    users: User

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UserUpdatePass(BaseModel):
    old_password: str
    new_password: str

class UserAuth(BaseModel):
    username: str
    password: str

