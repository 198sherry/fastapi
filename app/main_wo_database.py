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
        conn = psycopg2.connect(host ='localhost', database='fastapi', user='postgres', password ='w1i6f', cursor_factory = RealDictCursor)
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
    return {"data": my_posts}

#@app.post("/createposts")
#def create_posts(payload: dict = Body(...)):
#        print(payload)
#        return {"new_post": f"title {payload['title']} content {payload['content']}"}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post):

    print(new_post)
    post_dict = new_post.dict()
    print(post_dict)
    post_dict["id"]= randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data is ": my_posts}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/posts/{id}")
def get_post(id: int): #, response: Response):

    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return ("post detail:", post)

def find_post(id):
    print("in find_post: ", type(id))
    print(id)
    #print(my_posts)
    for post in my_posts:
        print("my_posts: ", post["id"])
        if post["id"] == id:
            return post
    return None

def find_index_post(id):
    print(f"id: {id}")
    for i, p in enumerate(my_posts):
        print(f"i: {i}, p['id']: {p['id']}")
        if p['id'] == id:
            return i
    return len(my_posts)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == len(my_posts):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        my_posts.pop(index)
        return #no other content can be sent for delete request other than status_code
          
@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post):
    index = find_index_post(id)
    if index == len(my_posts):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        new_entry = updated_post.dict()
        new_entry['id'] = id
        my_posts[index] = new_entry
    #     print(f"message with {id} is updated")
    return {'message': f"updated post {my_posts}"} #(f"message with {id} is update")