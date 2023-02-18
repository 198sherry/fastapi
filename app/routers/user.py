from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['Users']
)

@router.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
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

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)): #, response: Response):
    user = db.query(models.User).filter( models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message:': f"post with id: {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")

    return user #("post detail:", post)