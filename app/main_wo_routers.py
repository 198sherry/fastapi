from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Welcome to my world"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts#{"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**new_post.dict())
    #post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post # {"data is ": post}

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): #, response: Response):
    post = db.query(models.Post).filter( models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post #("post detail:", post)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter( models.Post.id == id) #.first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        post.delete(synchronize_session = False)
        db.commit()
        return #no other content can be sent for delete request other than status_code
          
@app.put("/posts/{id}")#, response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter( models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        post_query.update( updated_post.dict(), synchronize_session = False )
        db.commit()
        return (f"message with id {id} is update")

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash password
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    user = models.User(**new_user.dict())
    #post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user # {"data is ": post}

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)): #, response: Response):
    user = db.query(models.User).filter( models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")

    return user #("post detail:", post)