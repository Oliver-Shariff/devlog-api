from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import entries as entries_crud
from app.schemas import EntryCreate, EntryUpdate, TagRead
from pydantic import EmailStr
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/tags", tags=["tags"])

@router.get("/", response_model=list[TagRead])
async def get_tags():
    return True
