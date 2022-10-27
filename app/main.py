from asyncio.windows_events import NULL
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from . import schemas
from typing import List
from . import utils
from .routers import post,user,login,vote
#Imports for the sqlalchemy models
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .database import SessionLocal, engine,get_db
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)
# Dependency


# Imports for the database
import psycopg2
import time
from psycopg2.extras import RealDictCursor

# Defining the connection

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='root',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database succesfully connected.")
        break
    except Exception as e:
        print("DataBase connection failed.")
        print("Error : ",e)
        time.sleep(2)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)

@app.get("/")
def home():
    return 'Hello WOrld'


# if __name__ == "__main__":
#     # Use this for debugging purposes only
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")



