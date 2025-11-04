from pydantic import BaseModel, EmailStr
from datetime import datetime

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