from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import Tag, TagEntryJoin, Entry

def create_tag(name: str, user_email: str, db: Session):
    new_tag = Tag(name=name, user_email=user_email)
    try:
        db.add(new_tag)
        db.flush()
        db.refresh(new_tag)
        db.commit()
        return new_tag
    except IntegrityError:
        db.rollback()
        raise

def link_tag_to_entry(entry_id: int, user_email: str, tag_name, db: Session):
    tag = db.execute(
        select(Tag).filter_by(user_email=user_email, name=tag_name)
    ).scalar_one_or_none()

    if tag is None:
        raise ValueError("Tag not found for this user")

    entry = db.get(Entry, entry_id)
    if not entry or entry.user_email != user_email:
        raise ValueError("Entry not found or not owned by this user")

    new_link = TagEntryJoin(tag_id=tag.id, entry_id=entry.id)
    db.add(new_link)
    try:
        db.commit()
        db.refresh(new_link)
        return new_link
    except IntegrityError:
        db.rollback()
        raise

def get_entries_by_tag(tag_name: str, user_email: str, db: Session):
    tag = db.execute(
        select(Tag).filter_by(user_email=user_email, name=tag_name)
    ).scalar_one_or_none()
    if not tag:
        return []

    stmt = (
        select(Entry)
        .join(TagEntryJoin, Entry.id == TagEntryJoin.entry_id)
        .filter(TagEntryJoin.tag_id == tag.id)
        .order_by(Entry.created_on.desc())
    )
    return db.execute(stmt).scalars().all()
