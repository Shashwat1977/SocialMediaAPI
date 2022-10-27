from .. import schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils
from ..database import SessionLocal, engine,get_db
from .. import models
router = APIRouter(
    tags = ['User']
)

@router.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db : Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}",response_model=schemas.UserOut)
def get_user(id: int,db : Session = Depends(get_db)):
    usr = db.query(models.User).filter(models.User.id == id).first()
    if not usr: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given user with id : {id} was not found")
    else:
        return usr