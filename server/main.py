import src
from fastapi import FastAPI
from src.models import models
from src.database.database import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from src.routes import users, books

@app.get("/")
def read_root():
    return {"Hello": "World"}
