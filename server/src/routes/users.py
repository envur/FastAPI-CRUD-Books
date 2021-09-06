from fastapi import Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from main import *
from src.database.database import *
from src.cruds import users as u_cruds
from src.schemas import users as u_schemas
from src.schemas import status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/get", tags=["Users"], response_model=u_schemas.AllUsers)
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 0):
    db_users = u_cruds.get_users(db, skip, limit)
    db_users = jsonable_encoder(db_users)
    return JSONResponse(db_users)

@app.post("/user/register", tags=["Users"], response_model=u_schemas.User)
def create_user(user: u_schemas.UserCreate = Body(..., embed=True), db: Session = Depends(get_db)):
    db_user = u_cruds.create_user(db=db, user=user)
    return db_user

@app.post("/user/login", tags=["Users"], response_model=u_schemas.User)
def auth_user(user_credentials: u_schemas.UserAuth, db: Session = Depends(get_db)):
    return u_cruds.auth_user(db, user_credentials)

@app.put("/user/update/{user_id}", tags=["Users"], response_model=status.Status)
def update_user(user_id: int, items: u_schemas.UserUpdate = Body(..., embed=True), db: Session = Depends(get_db)):
    db_user = u_cruds.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    u_cruds.update_user(user_id=user_id, user=items, db=db)
    return status.Status(message="User updated successfully")

@app.delete("/user/delete/{user_id}", tags=["Users"], response_model=status.Status)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = u_cruds.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Couldn't delete the user!")
    db_user = u_cruds.delete_user(db, user_id=user_id)
    return status.Status(message="User was successfully deleted!")
