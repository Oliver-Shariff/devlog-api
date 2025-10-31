from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import user as users_crud


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/allUsers")
async def get_all_users_route(db: Session = Depends(get_db)):
    """This route returns all users"""
    users = users_crud.get_all_users(db)
    return users
