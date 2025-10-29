from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/status")
async def status():
    return {"status": "ok", "time": datetime.now()}