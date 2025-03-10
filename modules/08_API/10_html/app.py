from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


class Book(BaseModel):
    name: str = Field(examples=["Война и Мир"])
    author: str = Field(examples=["Л. Н. Толстой"])
    year: int = Field(examples=[1868])


books = [
    Book(name="Война и Мир", author="Л. Н. Толстой", year=1868),
    Book(name="Мцыри", author="М. Ю. Лермонтов", year=1839),
]


HOME_PAGE_HTML = """
<html>
    <head>
        <title>Главная</title>
        <link href="/static/style.css" rel="stylesheet" />
    </head>
    <body>
        <h1>Онлайн-библиотека</h1>
        <img width="500px" src="/static/library.jpg"/>
        <a href="/catalog">Перейти в каталог</a>
    </body>
</html>
"""

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))


@app.get("/")
async def home_page():
    return HTMLResponse(content=HOME_PAGE_HTML)


@app.get("/catalog")
async def catalog_page(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request, "books": books})
