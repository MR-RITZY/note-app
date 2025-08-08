from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False, 
                          server_default=func.now())
   
class NoteCategory(Base):
    __tablename__ = "note_categories"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_name = Column(String, nullable=False)
    
    note = relationship("Notes", back_populates="note_category")
    

class Notes(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("note_categories.id", ondelete="SET NULL"), 
                         nullable=True)
    date_created=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    date_modified=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), 
                           server_onupdate=func.now())
    bookmark = Column(Boolean, nullable=False, server_default="false")
    
    note_category = relationship("NoteCategory", back_populates="note")