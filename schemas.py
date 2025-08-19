from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserCreated(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
       from_attributes = True

class UserEdit(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class Token_data(BaseModel):
    user_id: int
    token_kind: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class RefreshToken(BaseModel):
    access_token: str
    token_type: str
    
class NoteCreated(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

    @field_validator("category_id")
    def set_default_category(cls, value):
        if value is None:
            value = 1
        elif value < 1:
            raise ValueError("category_id cannot less than 1")
        return value
    
class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    category_id: Optional[int] = None
    
    class Config:
        from_attributes = True
    
class CategorizedNote(BaseModel):
    id: int
    title: str
    content: str
    category_id: Optional[int] = None
    class Config:
        from_attributes = True
    
class BookmarkNote(BaseModel):
    id: int
    title: str
    content: str
    bookmark: bool
    
    class Config:
        from_attributes = True

class AllNoteOut(BaseModel):
    id: int
    title: str
    
    class Config:
        from_attributes = True  

class AllCategoryOut(BaseModel):
    id: int
    category_name: str
    
    class Config:
        from_attributes = True      

class EditNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    
class EditCategory(BaseModel):
    category_name: str
    
    @field_validator("category_name")
    def no_default_override(cls, value):
        if value.strip().title() == "Uncategorized":
            raise ValueError("Cannot name with default category name")
        return value.title()
    
class Deletion(BaseModel):
    detail: str

class PasswordUpdate(BaseModel):
    detail: str    

class CategoryCreated(BaseModel):
    category_name: str
    
    @field_validator("category_name")
    def no_default_override(cls, value):
        if value.strip().title() == "Uncategorized":
            raise ValueError("Cannot name with default category name")
        return value.title()
    
class ChangePassword(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)