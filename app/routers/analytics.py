from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.crud import entries as entries_crud
from app.schemas import EntryCreate, EntryUpdate, EntryRead
import app.security as security
from app.models import User
import app.analytics as analytics

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/overview")
async def get_analytics_overview(
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """Return a summary of entry/tag activity for the current user."""
    data = analytics.get_user_analytics(db=db, user_email=current_user.email)
    return data

@router.get("/activity")
async def get_activity(current_user: User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    """ Get the number of entries by date for the last 15 days """
    data = analytics.entries_by_date(db=db,user_email=current_user.email)
    return data