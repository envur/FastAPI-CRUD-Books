from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.models import books as b_models
from src.schemas import books as b_schemas


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(b_models.Books).offset(skip).limit(limit).all()

def get_books_by_user(db: Session, user_id: int):
    books_by_user = select(b_models.Books).filter_by(owner_id=user_id)
    books_by_user = db.execute(books_by_user).all()
    return books_by_user

def get_book_by_id(db: Session, book_id: int):
    db_book = db.query(b_models.Books).filter(b_models.Books.id == book_id).first()
    return db_book

def add_book(db: Session, user_id: int, book:b_schemas.BookRegister):
    db_book = b_models.Books(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, user_id:int, book: b_schemas.BookUpdate, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book.owner_id == user_id:
        db_book_update = update(b_models.Books).where(b_models.Books.id == book_id).values(**book.dict(exclude_unset=True))
        db.execute(db_book_update)
        db.commit()

def delete_book(db: Session, book_id: int, user_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book.owner_id == user_id:
        db.delete(db_book)
        db.commit()