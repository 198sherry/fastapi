from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#this is a Schema/Pydantic model, it defines the structure of a request & response 
# to ensure that when a user wants to create a post, the request will only go through 
# if it has a match content in the body
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host ='localhost', database='fastapi', user='postgres', 
        password ='w1i6f8', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database conneciton was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print('error:', error)
        time.sleep(2) # retry to connect to the server after 2 seconds


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, 
{"title": "title of post 2", "content": "content of post 2", "id":2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my world"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post, db: Session = Depends(get_db)):
    post = models.Post(**new_post.dict())
    #post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"data is ": post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)): #, response: Response):
    post = db.query(models.Post).filter( models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return ("post detail:", post)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter( models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        post.delete(synchronize_session = False)
        db.commit()
        return #no other content can be sent for delete request other than status_code
          
@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter( models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        post_query.update( updated_post.dict(), synchronize_session = False )
        db.commit()
    #     print(f"message with {id} is updated")
    return {'message': f"updated post {post}"} #(f"message with {id} is update")