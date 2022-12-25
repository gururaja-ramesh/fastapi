#uvicorn app.main:app --reload
from curses.ascii import HT
from pkgutil import ImpImporter
from this import s
from turtle import title
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user

# This creates a table in postgres based on the model we defined
# if the table already exists then it doesn't do anything
models.Base.metadata.create_all(bind=engine)

# connection to database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='anuguru', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {'message': 'welcome to my api!!!!!'}