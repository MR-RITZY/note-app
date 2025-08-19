from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, models, schemas, utils, oauth2

router = APIRouter(prefix="/user", tags=["Account Creation"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_account(user: schemas.UserCreated, db: Session = Depends(database.get_db)):
    
    existing_user = db.query(models.Users).filter_by(email = user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="An account with this email already exists")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.model_dump(),
                            note_categories=[models.NoteCategory
                                             (category_name="Uncategorized")])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/view/me", response_model=schemas.UserOut)
def get_user(current_user = Depends(oauth2.get_current_user)):
   
    return current_user

@router.put("/edit/me", response_model=schemas.UserOut)
def edit_user(user: schemas.UserEdit, db: Session = Depends(database.get_db),
             current_user = Depends(oauth2.get_current_user)):
    query = db.query(models.Users).filter_by(id = current_user.id)
    query.update(user.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return query.first()

@router.delete("/delete/me", response_model=schemas.Deletion)
def delete_me(db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    query = db.query(models.Users).filter_by(id = current_user.id)
    query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Account successfully deleted"}

@router.put("/change-password", response_model=schemas.PasswordUpdate)
def change_password(payload: schemas.ChangePassword, 
                    db: Session = Depends(database.get_db), 
                    current_user = Depends(oauth2.get_current_user)):

    if not utils.verify(payload.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current password is incorrect"
        )
    
    if utils.verify(payload.new_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current password"
        )

    current_user.password = utils.hash(payload.new_password)
    db.commit()

    return {"detail": "Password updated successfully"}