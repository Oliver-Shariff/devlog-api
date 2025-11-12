from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select, func
from app.models import Entry, Tag, TagEntryJoin
import json
def get_user_analytics(db: Session, user_email: str):
    # ---  Total entries ---
    total_entries_stmt = (
        select(func.count().label("total_entries"))
        .select_from(Entry)
        .filter(Entry.user_email == user_email)
    )
    total_entries = db.execute(total_entries_stmt).scalar_one()

    # --- Total tags used by user ---
    subq = select(Entry.id).filter(Entry.user_email == user_email)
    total_tags_stmt = (
        select(func.count().label("total_tags"))
        .select_from(TagEntryJoin)
        .filter(TagEntryJoin.entry_id.in_(subq))
    )
    total_tags = db.execute(total_tags_stmt).scalar_one()

    # --- Entries per tag ---
    entries_per_tag_stmt = (
        select(Tag.name, func.count(Entry.id).label("entries_per_tag"))
        .join(TagEntryJoin, TagEntryJoin.tag_id == Tag.id)
        .join(Entry, Entry.id == TagEntryJoin.entry_id)
        .filter(Entry.user_email == user_email)
        .group_by(Tag.name)
        .order_by(func.count(Entry.created_on).desc())
    )
    entries_per_tag = [
        {"tag": name, "count": count} for name, count in db.execute(entries_per_tag_stmt)
    ]

    return {
        "total_entries": total_entries,
        "total_tags": total_tags,
        "entries_per_tag": entries_per_tag,
    }

def entries_by_date(db:Session, user_email: str):
    stmnt = (
        select(func.date_trunc('day',Entry.created_on).label("date"), func.count().label("entries"))
        .select_from(Entry)
        .filter(Entry.user_email == user_email)
        .group_by(func.date_trunc('day',Entry.created_on))
        .order_by(func.date_trunc('day',Entry.created_on).desc())
        .limit(15)
    )
    results = db.execute(stmnt).all()
    data = {
        (row.date.date().isoformat() if hasattr(row.date, "date") else str(row.date)): row.entries
        for row in results
    }

    return data
#    entries_per_date = [
#        {created_on: entries} for created_on, entries in db.execute(stmnt)
#    ]
#
#    return entries_per_date
