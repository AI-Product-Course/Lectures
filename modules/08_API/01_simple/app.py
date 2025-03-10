from fastapi import FastAPI


app = FastAPI(title="Hello application")

@app.get("/")
def home():
    return {"message": "Hello"}
