from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from config import settings
import database, models, schemas

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
refresh_Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/refresh")


def create_token(data: dict, expires_delta: timedelta, token_kind: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "token_kind": token_kind})
    return jwt.encode(to_encode, settings.secret, algorithm=settings.algorithm)

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=settings.access_time), token_kind="access_token")

def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=settings.refresh_time), token_kind="refresh_token")

def verify_token(token, credential_exception):
    try:
        payload = jwt.decode(token, settings.secret, settings.algorithm)
        user = payload.get("user_id")
        if user is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    token_data = schemas.Token_data(user_id=user, token_kind=payload.get("token_kind"))
    return token_data

def check_token_kind(token_kind: str, expected_token_kind: str, credential_exception):
    if token_kind != expected_token_kind:
        raise credential_exception
    
def get_current_user(token:str = Depends(Oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    
    user_data = verify_token(token, credential_exception)
    check_token_kind(user_data.token_kind,"access_token", credential_exception)

    user = db.query(models.Users).filter_by(id = user_data.user_id).first()
    if user is None:
        raise credential_exception
    return user

def get_current_user_from_refresh(token:str = Depends(refresh_Oauth2_scheme), 
                                  db: Session = Depends(database.get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    
    user_data = verify_token(token, credential_exception)
    check_token_kind(user_data.token_kind,"refresh_token", credential_exception)
    
    user = db.query(models.Users).filter_by(id = user_data.user_id).first()
    if user is None:
        raise credential_exception
    return user