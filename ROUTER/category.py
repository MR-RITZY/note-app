from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, database, oauth2, models

router = APIRouter(prefix="/category", tags=["Categories"])


@router.post("/create")
def create_category(category: schemas.CategoryCreated, db: Session = Depends(database.get_db), 
                    current_user = Depends(oauth2.get_current_user)):
    existing_category = db.query(models.NoteCategory).filter_by(category_name= category.category_name, 
                                                                user_id = current_user.id).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Category already exists")
    new_category = models.NoteCategory(user_id=current_user.id, 
                                       category_name=category.category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/all", response_model=List[schemas.AllCategoryOut])
def get_categories(db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
   categories = db.query(models.NoteCategory).filter_by(user_id=current_user.id).all()
   return categories

@router.get("/{category_id}", response_model=List[schemas.AllNoteOut])
def get_category_note(category_id: int, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
    category = db.query(models.NoteCategory).filter_by(id = category_id, 
                                                      user_id = current_user.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category doesn't exist") 
    notes = category.note
    return notes


@router.put("/edit/{category_id}")
def edit_category(category_id: int, category: schemas.EditCategory, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):

    category_query = db.query(models.NoteCategory).filter_by(id=category_id, user_id=current_user.id)
    editing_category = category_query.first()
    if not editing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist")
    
    if editing_category.category_name == "Uncategorized":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot edit default category")

    category_query.update(category.model_dump(), synchronize_session=False)
    db.commit()
    edited_category = category_query.first()
    return edited_category


@router.delete("/delete/{category_id}", response_model=schemas.Deletion)
def delete_category(category_id:int, db: Session = Depends(database.get_db), 
                    current_user = Depends(oauth2.get_current_user)):

    category_query = db.query(models.NoteCategory).filter_by(id=category_id, user_id=current_user.id)
    category = category_query.first()
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist")

    if category.category_name == "Uncategorized":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete default category")
   
    category_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Category deleted successfully"}