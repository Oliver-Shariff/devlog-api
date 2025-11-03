from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import users as users_crud
from datetime import datetime



router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/allUsers")
async def get_all_users_route(db: Session = Depends(get_db)):
    """This route returns all users"""
    users = users_crud.get_all_users(db)
    return users

@router.get("/{user_email}")
async def get_user( user_email, db: Session = Depends(get_db)):
    """ This route returns a user from an input email """
    user = users_crud.get_user(user_email, db)
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return user

@router.post("/", status_code=201)
async def add_user(new_user:dict, db: Session = Depends(get_db)):
    """ This route adds a new user """
    # Extract fields from the incoming JSON body
    email = new_user.get("email")
    username = new_user.get("username")
    password = new_user.get("password")

    try:
        created = users_crud.add_user(
            email=email,
            username=username,
            password=password,
            created_on=datetime.now(),
            db=db
        )
        data = jsonable_encoder(created)
        data.pop("password", None)

        return (data)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exsits"
        )

@router.put("/{user_email}")
async def change_password(user_email, password: dict, db:Session = Depends(get_db)):
    """ This route changes a user's password """
    password = password.get("password")
    users_crud.change_password(user_email,password,db)
    return {"message": f"password changed to {password} successfully."}

@router.delete("/{user_email}")
async def deleter_user(user_email, db:Session = Depends(get_db)):
    """ This route deletes a user """
    user = users_crud.delete_user(user_email, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return {"message": f"user {user_email} deleted successfully."}