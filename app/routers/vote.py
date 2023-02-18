from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/vote', 
    tags =['Vote'] #about the documentation
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def votes(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #print(vote.post_id, vote.dir)
    post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} doesn't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}