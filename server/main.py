import src
from fastapi import FastAPI
from src.models import models
from src.database.database import *

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.routes import users, books

@app.get("/", tags=["Root"])
def Hello_World():
    return {"Hello": "World"}
