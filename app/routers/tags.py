from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import tags as tags_crud
from app.schemas import EntryCreate, EntryUpdate, TagRead, EntryRead, TagCreate
from pydantic import EmailStr
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/tags", tags=["tags"])

@router.post("/", response_model=TagRead, status_code=201)
async def create_tag(new_tag: TagCreate, current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    created = tags_crud.create_tag(name=new_tag.name, user_email=current_user.email, db=db)
    return created

@router.post("/{entry_id}/{tag_name}", status_code=204)
async def link_tag(entry_id: int, tag_name: str, current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    return tags_crud.link_tag_to_entry(entry_id=entry_id, user_email=current_user.email,tag_name=tag_name,db=db)


@router.get("/{tag_name}", response_model=list[EntryRead])
async def get_entries_by_tag(tag_name: str, current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    """ Get all entries with input tag """
    entries = tags_crud.get_entries_by_tag(tag_name=tag_name, user_email= current_user.email,db=db)
    if entries is None:
        raise HTTPException(status_code=404, detail = "No entries with this tag.")
    return entries

