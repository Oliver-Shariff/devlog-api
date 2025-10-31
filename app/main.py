from fastapi import FastAPI
from datetime import datetime
from app.models import Base
from app.database import engine

app = FastAPI()

@app.get("/hello")
async def hello():
    """This route returns Hello World"""
    return {"message": "Hello World"}


@app.get("/status")
async def status():
    """ This route returns the status and current time. Status is set statically at the moment """
    return {"status": "ok", "time": datetime.now()}

Base.metadata.create_all(bind=engine)