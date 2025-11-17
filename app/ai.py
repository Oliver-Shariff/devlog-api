from sqlalchemy.orm import Session
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

def summarize_entry_text(entry_id: int, user_email, db: Session ) -> str:
    entry = db.get(Entry, entry_id)

    if not entry or entry.user_email != user_email:
        return None
    
    entry_text = entry.content
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes user journal entries into concise reflections."},
            {"role":"user", "content": f"Summarize this entry in 2-3 scentences:\n\n{entry_text}"}
        ],
        temperature=0.7,
        max_tokens=150,
    )

    summary = response.choices[0].message.content.strip()
    return summary

