from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, models, schemas, utils, oauth2

router = APIRouter(prefix="/user", tags=["Authencation"])

@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user_exist = db.query(models.Users).filter(models.Users.email == user.username).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    is_correct_password = utils.verify(user.password, user_exist.password)
    if not is_correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    token_data = {"user_id":user_exist.id}
    access_token = oauth2.create_access_token(token_data)
    refresh_token = oauth2.create_refresh_token(token_data)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=schemas.RefreshToken)
def refresh_token(user = Depends(oauth2.get_current_user_from_refresh)):
    
    token_data = {"user_id": user.id}
    new_access_token = oauth2.create_access_token(token_data)
  
    return {"access_token": new_access_token, "token_type": "bearer"}