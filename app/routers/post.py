from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix = '/posts', 
    tags =['Post'] #about the documentation
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] =""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).filter(
        models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()
    print(results)
    return results #posts#{"data": posts}

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id = current_user.id, **new_post.dict())
    #post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post # {"data is ": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #, response: Response):
    #post = db.query(models.Post).filter( models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id ).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).filter(
        models.Post.id == id, models.Post.owner_id == current_user.id ).group_by(models.Post.id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post #("post detail:", post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    post_query = db.query(models.Post).filter( models.Post.id == id) #.first()
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="not authorized")

    post_query.delete(synchronize_session = False)
    db.commit()
    return #no other content can be sent for delete request other than status_code
          
@router.put("/{id}")#, response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    post_query = db.query(models.Post).filter( models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"not authorized")
    
    post_query.update( updated_post.dict(), synchronize_session = False )
    db.commit()
    return (f"message with id {id} is update")