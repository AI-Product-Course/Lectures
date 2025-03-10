import time
from fastapi import FastAPI


app = FastAPI(title="Sync application")

@app.get("/")
def home():
    time.sleep(0.5)
    return {"message": "Hello"}
