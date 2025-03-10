import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, Path, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


UPLOAD_DIRECTORY = "uploads"
FILE_MAX_SIZE = 2 * 1024 * 1024 # Mb


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


class SuccessMessage(BaseModel):
    message: str = Field(examples=["Операция успешно выполнена"])


app = FastAPI()


@app.post(
    "/files", description="Upload file",
    response_description="File successfully uploaded", response_model=SuccessMessage, status_code=201
)
async def upload_file(file: UploadFile = File(...)):
    if file.size > FILE_MAX_SIZE:
        raise HTTPException(status_code=400, detail="Файл слишком большой")
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Файл с таким названием уже существует")
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return SuccessMessage(message=f"Файл сохранен и доступен по пути: {file_path}")


@app.get(
    "/files/{filename}", description="Download file",
    response_description="File successfully downloaded", response_model=FileResponse, status_code=200
)
async def download_file(filename: str = Path()):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(path=file_location, filename=filename)
