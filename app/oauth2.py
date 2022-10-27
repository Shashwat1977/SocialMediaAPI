from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .database import get_db
from . import models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM =settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expiry = datetime.utcnow()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expiry})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encode_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials",
    headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
