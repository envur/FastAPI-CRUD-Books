from fastapi import Body, Depends, HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from main import *
from src.database.database import *
from src.cruds import books as b_cruds
from src.schemas import books as b_schemas
from src.schemas import status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books/get", tags=["Books"], response_model=List[b_schemas.AllBooks])
def get_books(skip: int = 0, limit = 100, db: Session = Depends(get_db)):
    db_books = b_cruds.get_books(db, skip, limit)
    db_books = jsonable_encoder(db_books)
    return JSONResponse(db_books)

@app.get("/user/{user_id}/books/get", tags=["Books"], response_model=List[b_schemas.AllBooks])
def get_books_by_user(user_id: int, db: Session = Depends(get_db)):
    db_books = b_cruds.get_books_by_user(db, user_id)
    db_books = jsonable_encoder(db_books)
    return JSONResponse(db_books)

@app.post("/user/{user_id}/book/add", tags=["Books"], response_model=b_schemas.Book)
def add_book(user_id: int, book: b_schemas.BookRegister = Body(..., embed=True), db: Session = Depends(get_db)):
    db_book = b_cruds.add_book(db, user_id, book)
    return(db_book)

@app.put("/user/{user_id}/book/update/{book_id}", tags=["Books"], response_model=status.Status)
def update_book(user_id: int, book: b_schemas.BookUpdateRequest, book_id: int, db: Session = Depends(get_db)):
    db_book = b_cruds.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail="Couldn't update the specified book")
    db_book = b_cruds.update_book(db, user_id, book, book_id)
    return status.Status(message="Book successfully updated")

@app.delete("/user/{user_id}/book/delete/{book_id}", tags=["Books"], response_model=status.Status)
def delete_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    db_book = b_cruds.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail="Couldn't delete the specified book")
    db_book = b_cruds.delete_book(db, book_id, user_id)
    return status.Status(message="Book successfully deleted")
