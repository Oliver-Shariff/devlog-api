from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

""" This route returns Hello World  """
@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


""" This route returns the status and current time. Status is set statically at the moment """
@app.get("/status")
async def status():
    return {"status": "ok", "time": datetime.now()}