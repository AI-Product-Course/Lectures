from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Hello application")


class HomeResponse(BaseModel):
    message: str = Field(examples=["Hello"])


@app.get(
    "/", description="Greeting message",
    response_description="Successful message", response_model=HomeResponse, status_code=200
 )
def home():
    return HomeResponse(message="Hello")
