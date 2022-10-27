from .. import schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils
from ..database import SessionLocal, engine,get_db
from .. import models
from .. import oauth2
router = APIRouter(
    tags = ['Auth']
)

@router.post("/login")
def login(user_auth:schemas.UserLogin,db : Session = Depends(get_db)):
    usr = db.query(models.User).filter(models.User.email == user_auth.email).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not utils.verify(user_auth.password,usr.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id":usr.id})
    return {"token":access_token,
            "token_type":"bearer"}