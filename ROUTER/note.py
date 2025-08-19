from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, database, oauth2, models

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/create", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreated, db: Session = Depends(database.get_db),
                current_user = Depends(oauth2.get_current_user)):
    
    existing_category = db.query(models.NoteCategory).filter_by(
                        id=note.category_id, user_id=current_user.id).first()

    if not existing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist")
        
    new_note = models.Notes(user_id=current_user.id, **note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

        
@router.get("/all", response_model=List[schemas.AllNoteOut])
def get_all_notes(db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
   notes = db.query(models.Notes).filter_by(user_id=current_user.id).all()
   return notes

@router.get("/uncategorized", response_model=List[schemas.AllNoteOut])
def get_uncategorized(db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    
    uncategorized_category = db.query(models.NoteCategory).filter_by(
        user_id=current_user.id, category_name="Uncategorized").first()
    
    if not uncategorized_category:
        return []  # fallback, just in case

    uncategorized_notes = uncategorized_category.notes
    return uncategorized_notes

@router.get("/bookmarks", response_model=List[schemas.AllNoteOut])
def get_bookmark(db: Session = Depends(database.get_db), 
                 current_user = Depends(oauth2.get_current_user)):
    
    notes = db.query(models.Notes).filter_by(bookmark=True, user_id=current_user.id).all()
    return notes

@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
    note = db.query(models.Notes).filter_by(id = note_id, user_id = current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"Note with id: {note_id} not found")
    return note

@router.put("/edit/{note_id}", response_model=schemas.NoteOut)
def edit_note(note_id: int, note: schemas.EditNote, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
    note_query = db.query(models.Notes).filter_by(id = note_id, user_id = current_user.id)
    editing_note = note_query.first()
    if not editing_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"Note with id: {note_id} not found")
        
    note_query.update(note.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    edited_note = note_query.first()
    return edited_note


@router.delete("/delete/{note_id}", response_model=schemas.Deletion)
def delete_note(note_id:int, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    
    note_query = db.query(models.Notes).filter_by(id = note_id, user_id=current_user.id)
    note = note_query.first()
    
    if not note:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"Note with id: {note_id} not found")
   
    note_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Note deleted successfully"}
    
@router.put("/bookmark/{note_id}", response_model=schemas.BookmarkNote)
def toggle_bookmark(note_id: int, db: Session = Depends(database.get_db), 
                  current_user = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Notes).filter_by(id=note_id, user_id=current_user.id)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Note with id: {note_id} not found")
    note_query.update({"bookmark": not note.bookmark}, synchronize_session=False)
    db.commit()
    bookmarked_note = note_query.first()
    return bookmarked_note

@router.put("/category/{note_id}/{category_id}", response_model=schemas.CategorizedNote)
def categorize(note_id: int, category_id: int, db: Session = Depends(database.get_db), 
               current_user = Depends(oauth2.get_current_user)):

    note = db.query(models.Notes).filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Note with id: {note_id} not found")

    if note.category_id == category_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Note already in category")

    category = db.query(models.NoteCategory).filter_by(id=category_id, 
                                                       user_id=current_user.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category doesn't exist")

    note.category_id = category_id
    db.commit()
    db.refresh(note) 
    return note