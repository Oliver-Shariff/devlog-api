from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import Tag, TagEntryJoin, Entry

def create_tag(name: str, user_email: str, db: Session):
    new_tag = Tag(name = name, user_email = user_email)
    try:
        db.commit()
        db.refresh(new_tag)
        return(new_tag)
    except IntegrityError:
        db.rollback()
        raise

def link_tag_to_entry(entry_id: int, user_email: str, tag_name, db: Session):
    stmnt = select(Tag).filter_by(user_email= user_email).filter(tag_name=tag_name)
    tag = db.execute(stmnt)
    new_tag_entry_join = TagEntryJoin(tag_id = tag.id, entry_id=entry_id)
    db.add(new_tag_entry_join)
    try:
        db.commit()
        db.refresh(new_tag_entry_join)
        return(new_tag_entry_join)
    except IntegrityError:
        db.rollback()
        raise

def get_entries_by_tag(tag_name: str, user_email: str, db: Session):
    stmnt = select(Tag).filter_by(user_email= user_email).filter(tag_name=tag_name)
    tag = db.execute(stmnt)
    stmnt = select(Entry).filter_by(tags = tag.id)
    result = db.execute(stmnt)
    return result.scalars().all()
