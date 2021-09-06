from typing import Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    read: bool

class BookRegister(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    read: Optional[bool] = None

class AllBooks(BaseModel):
    books: Book