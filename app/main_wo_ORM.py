from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

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

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()

    return {"data is ": post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/posts/{id}")
def get_post(id: int): #, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return ("post detail:", post)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        conn.commit()
        return #no other content can be sent for delete request other than status_code
          
@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post):
    cursor.execute("""UPDATE posts SET title =%s, content =%s, published =%s WHERE id = %s RETURNING *""",
     (updated_post.title, updated_post.content, updated_post.published, str(id)))

    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        conn.commit()
    #     print(f"message with {id} is updated")
    return {'message': f"updated post {post}"} #(f"message with {id} is update")