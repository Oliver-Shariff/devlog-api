from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
import app.ai as ai_functions
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/summarize/{entry_id}")
async def summarize_entry(entry_id: int, db: Session= Depends(get_db), current_user: User = Depends(security.get_current_user)):
    summary = ai_functions.summarize_entry_text(entry_id=entry_id, user_email=current_user.email, db=db)

    if not summary:
        raise HTTPException(status_code=404, detail = "Entry does not exist or does not belong to you.")
    return summary