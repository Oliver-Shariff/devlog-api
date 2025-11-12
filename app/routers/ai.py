from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import entries as entries_crud
from app.schemas import EntryCreate, EntryUpdate, EntryRead
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/ai", tags=["ai"])
