from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select
from app.models import Entry

def create_entry(user_email, title, content, db: Session):
    new_entry = Entry(user_email = user_email, title = title, content = content)
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
        return(new_entry)
    except IntegrityError:
        db.rollback()
        raise

def get_entry_by_id(entry_id, user_email, db: Session):
    entry = db.get(Entry, entry_id)
    owner = getattr(entry, "user_email")
    if owner != user_email:
        return None
    return entry

def get_entries_for_user(user_email, db: Session, skip: int, limit: int):
    stmnt = (
        select(Entry)
        .filter_by(user_email = user_email)
        .order_by(Entry.created_on.desc())
        .offset(skip)
        .limit(limit))
    result = db.execute(stmnt)
    return result.scalars().all()

def update_entry(entry_id, db: Session, user_email, title = None, content = None,):
    entry = db.get(Entry, entry_id)
    owner = getattr(entry, "user_email")
    if owner != user_email or entry is None:
        return None
    if title is None:
        title = getattr(entry, "title")
    if content is None:
        content = getattr(entry, "content")
    stmnt = update(Entry).where(Entry.id == entry_id).values(title = title, content = content)
    db.execute(stmnt)
    db.commit()
    db.refresh(entry)
    return True

def delete_entry(entry_id,user_email, db: Session):
        entry = db.get(Entry, entry_id)
        owner = getattr(entry, "user_email")
        if owner != user_email or entry is None:
            return None
        db.delete(entry)
        db.commit()
        return True