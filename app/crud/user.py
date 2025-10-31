from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User

def get_all_users(db: Session):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()
