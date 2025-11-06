from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import users as users_crud
from app.schemas import UserCreate, UserUpdate, UserRead, Token
from pydantic import EmailStr
import app.security as security


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_all_users_route(db: Session = Depends(get_db)):
    """This route returns all users"""
    users = users_crud.get_all_users(db)
    return users

@router.get("/{user_email}", response_model=UserRead)
async def get_user( user_email:EmailStr, db: Session = Depends(get_db)):
    """ This route returns a user from an input email """
    user = users_crud.get_user(user_email, db)
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return user

@router.post("/",response_model=UserRead, status_code=201)
async def add_user(new_user:UserCreate, db: Session = Depends(get_db)):
    """ This route adds a new user """
    try:
        created = users_crud.add_user(
            email=new_user.email,
            username=new_user.username,
            password=new_user.password,
            created_on=datetime.now(),
            db=db
        )
        return (created)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

@router.put("/{user_email}", status_code=204)
async def change_password(user_email: EmailStr, password: UserUpdate, db: Session = Depends(get_db)):
    """This route changes a user's password."""
    new_password = password.password
    ok = users_crud.change_password(user_email, new_password, db)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return

@router.delete("/{user_email}", status_code=204)
async def delete_user(user_email:EmailStr, db:Session = Depends(get_db)):
    """ This route deletes a user """
    user = users_crud.delete_user(user_email, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return
