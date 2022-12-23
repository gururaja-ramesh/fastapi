#uvicorn app.main:app --reload
from curses.ascii import HT
from pkgutil import ImpImporter
from this import s
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# This creates a table in postgres based on the model we defined
# if the table already exists then it doesn't do anything
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

""" schema to enforce the data sent from frontend
in this case we use pydantic which also validates the data
example: title cannot be empty which will checked by pydantic
in this case published can be empty coz it has a default value """
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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



# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1},
# {"title": "favorite food", "content": "I like pizza", "id" : 2}
# ]

# def find_posts(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/")
def root():
    return {'message': 'welcome to my api!!!!!'}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "success"}

# get all posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data" : posts}

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

# get one post using id
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    return {"post_detail": post}

# Delete a post using the id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT) #204_no_content coz it is practise to not send any data after a delete request

# Update the contents of a post using id
@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist")
    conn.commit()
    return {'data': updated_post} 

