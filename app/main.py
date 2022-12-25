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

# This creates a table in postgres based on the model we defined
# if the table already exists then it doesn't do anything
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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

# get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) #unpacks the post like the above statement
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get one post using id
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    return post

# Delete a post using the id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #204_no_content coz it is practise to not send any data after a delete request

# Update the contents of a post using id
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    # RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# create a new users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) #unpacks the user info like the above statement
    db.add(new_user) 
    db.commit()
    db.refresh(new_user) # returns the recently created user from DB

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} does not exist") 
    return user