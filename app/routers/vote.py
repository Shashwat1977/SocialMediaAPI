from .. import schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import utils
from ..database import SessionLocal, engine,get_db
from .. import models
from .. import oauth2

router = APIRouter(
    tags=['Vote']
)

@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given post does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f"The given post is already liked by user.")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Succefully Voted"}
    else :
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"The given post is already liked by user.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"messgae":"Succesfully removed the vote"}