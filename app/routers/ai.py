from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
import app.ai as ai_functions
import app.security as security
from app.models import User

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/summarize/{entry_id}")
async def summarize_entry(entry_id: int,background_tasks: BackgroundTasks, db: Session= Depends(get_db), current_user: User = Depends(security.get_current_user) ):

    entry_text = ai_functions.validate_entry(entry_id=entry_id,user_email=current_user.email)

    if isinstance(entry_text, dict) and "error" in entry_text:
        raise HTTPException(status_code=entry_text["code"], detail=entry_text["error"])
    
    background_tasks.add_task(ai_functions.summarize_entry_text,entry_id=entry_id, entry_text=entry_text, db=db)

        
    return {"status": "processing"}