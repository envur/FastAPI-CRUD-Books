from sqlalchemy.orm import Session, query
from sqlalchemy import update
from src.models import users as u_models
from src.schemas import users as u_schemas
from src.schemas import status
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

def change_user_password(db: Session, user: u_schemas.UserUpdatePass, user_id: int):
    fake_hash_pass = user.new_password + "hash"
    db_user = update(u_models.User).where(u_models.User.id == user_id).values(hashed_password = fake_hash_pass)
    db.execute(db_user)
    db.commit()

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db=db, id=user_id)
    db.delete(db_user)
    db.commit()

def auth_user(db: Session, user_credentials: u_schemas.UserAuth):
    user_credentials.password = user_credentials.password + "hash"
    db_user = db.query(u_models.User).filter(u_models.User.username == user_credentials.username).first()
    if not db_user:
        return status.Status(message="User doesn't exist")
    print(user_credentials.password)
    if db_user.hashed_password == user_credentials.password:
        return db_user
    if db_user.hashed_password != user_credentials.password:
        return status.Status(message="Username or password is invalid")