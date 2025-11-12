from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import entries as entries_crud
from app.schemas import EntryCreate, EntryUpdate, EntryRead
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/entries", tags=["entries"])

@router.get("/", response_model=list[EntryRead])
async def get_current_user_entry(tag_name:str = None, current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """ This route returns all entries for the current user """
    entries = entries_crud.get_entries_for_user(
        current_user.email,
        db = db,
        tag_name= tag_name,
        skip = skip,
        limit=limit)
    return entries

@router.post("/", response_model=EntryRead, status_code=201)
async def create_entry(new_entry:EntryCreate, db: Session = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    """ This route adds an entry """
    created = entries_crud.create_entry(
        user_email = current_user.email,
        title = new_entry.title,
        content = new_entry.content,
        db = db
    )
    return created
    
@router.get("/{entry_id}", response_model=EntryRead)
async def get_entry_by_id(entry_id: int, current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    entry = entries_crud.get_entry_by_id(entry_id, current_user.email, db)
    if entry is None:
        raise HTTPException(status_code=404, detail = "Entry does not exist or does not belong to you.")
    return entry

@router.patch("/{entry_id}", status_code=204)
async def update_entry(entry_id: int, updated_entry: EntryUpdate, current_user: User = Depends(security.get_current_user), db:Session = Depends(get_db)):
    ok = entries_crud.update_entry(
        entry_id=entry_id,
        db = db,
        user_email = current_user.email,
        title = updated_entry.title,
        content = updated_entry.content)
    if not ok:
        raise HTTPException(status_code=404, detail="Entry not found or does not belong to you")
    return

@router.delete("/{entry_id}", status_code=204)
async def delete_entry(entry_id: int, current_user: User = Depends(security.get_current_user), db:Session = Depends(get_db)):
    entry = entries_crud.delete_entry(entry_id, current_user.email, db=db)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found or does not belong to you")
    return
