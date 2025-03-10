import asyncio
from fastapi import FastAPI


app = FastAPI(title="Async application")

@app.get("/")
async def home():
    await asyncio.sleep(0.5)
    return {"message": "Hello"}
