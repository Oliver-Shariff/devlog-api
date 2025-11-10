# def create_tag(name: str, db: Session):
#     ...
#
# def link_tag_to_entry(entry_id: int, tag_name: str, db: Session):
#     ...
#
# def get_entries_by_tag(user_email: str, tag_name: str, db: Session):
#     ...

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select
from app.models import Tag

def create_tag(name: str, user_email: str, db: Session):
    new_tag = Tag(name = name, user_email = user_email)
    try:
        db.commit()
        db.refresh(new_tag)
        return(new_tag)
    except IntegrityError:
        db.rollback()
        raise

def link_tag_to_entry(entry_id: int, user_email: str)
