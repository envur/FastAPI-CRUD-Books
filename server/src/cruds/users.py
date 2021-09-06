from sqlalchemy.orm import Session
from sqlalchemy import update
from src.models import users as u_models
from src.schemas import users as u_schemas
from src.cruds import books as b_cruds

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(u_models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(u_models.User).filter(u_models.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(u_models.User).filter(u_models.User.id == id).first()

def create_user(db: Session, user: u_schemas.UserCreate):
    fake_hash_pass = user.password + "hash"
    user_dict = user.dict()
    del user_dict['password']
    db_user = u_models.User(**user_dict, hashed_password = fake_hash_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: u_schemas.UserUpdate, user_id: int):
    db_user = update(u_models.User).where(u_models.User.id == user_id).values(**user.dict(exclude_unset=True))
    db.execute(db_user)
    db.commit()

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db=db, id=user_id)
    db.delete(db_user)
    db.commit()
