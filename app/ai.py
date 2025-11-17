from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from app.models import Entry
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_SUMMARIZE_KEY = os.getenv("OPENAI_SUMMARIZE_KEY")

client = OpenAI(
    api_key=OPENAI_SUMMARIZE_KEY
)

MIN_ENTRY_TEXT = 300

def summarize_entry_text(entry_id: int, user_email, db: Session ) -> str:
    entry = db.get(Entry, entry_id)

    summary = entry.summary
    if summary:
        return summary

    if not entry or entry.user_email != user_email:
        return None
    
    entry_text = entry.content

    if len(entry.content or "") <= MIN_ENTRY_TEXT:
        return {"error": f"Entry too short for summarization (min {MIN_ENTRY_TEXT} characters required)"}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes user journal entries into concise reflections."},
            {"role":"user", "content": f"Summarize this entry in 2-3 sentences:\n\n{entry_text}"}
        ],
        temperature=0.7,
        max_tokens=150,
    )

    summary = response.choices[0].message.content.strip()
    stmnt = update(Entry).where(Entry.id == entry_id).values(summary = summary)
    db.execute(stmnt)
    db.commit()
    db.refresh(entry)
    return summary

