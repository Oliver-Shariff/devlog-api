from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- User Schemas ---

class UserCreate(BaseModel):
    email:EmailStr
    username: str
    password: str

class UserRead(BaseModel):
    email: EmailStr
    username: str
    created_on: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    password: str

# --- Auth Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Tag Schemas ---

class TagBase(BaseModel):
    name: str
    email: EmailStr

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    class Config:
        from_attributes = True
        
# --- Entry Schemas ---

class EntryCreate(BaseModel):
    title: str
    content: str

class EntryRead(BaseModel):
    id: int
    title: str
    content: str
    created_on: datetime
    last_edit: datetime
    tags: list[TagRead] = []

    class Config:
        from_attributes = True

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
