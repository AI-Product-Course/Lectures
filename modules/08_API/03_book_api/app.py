from fastapi import FastAPI, Query, Body, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
from uuid import uuid4, UUID

app = FastAPI()

DATA_FILE = 'books.json'

class Book(BaseModel):
    id: UUID = Field(examples=[uuid4()])
    name: str = Field(examples=["Война и Мир"])
    author: str = Field(examples=["Л. Н. Толстой"])
    year: int = Field(examples=[1868])
    annotation: str = Field(examples=["Классический роман-эпопея рассказывает о сложном, бурном периоде в истории России и всей Европы с 1805 по 1812 год. "])


class CreateBook(BaseModel):
    name: str = Field(examples=["Война и Мир"])
    author: str = Field(examples=["Л. Н. Толстой"])
    year: int = Field(examples=[1868])
    annotation: str = Field(examples=["Классический роман-эпопея рассказывает о сложном, бурном периоде в истории России и всей Европы с 1805 по 1812 год. "])


class UpdateBook(BaseModel):
    name: str = Field(examples=["Война и Мир"])
    author: str = Field(examples=["Л. Н. Толстой"])
    year: int = Field(examples=[1868])
    annotation: str = Field(examples=["Классический роман-эпопея рассказывает о сложном, бурном периоде в истории России и всей Европы с 1805 по 1812 год. "])


class SuccessMessage(BaseModel):
    message: str = Field(examples=["Операция успешно выполнена"])


def load_books() -> list[Book]:
    books = []
    if not os.path.exists(DATA_FILE):
        return books
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        raw_list = json.load(f)
    for raw_data in raw_list:
        book_id = UUID(raw_data["id"])
        updated_raw_data = {**raw_data, "id": book_id}
        books.append(Book(**updated_raw_data))
    return books


def save_books(books: list[Book]):
    data = [{**book.model_dump(exclude={"id"}), "id": str(book.id)} for book in books]
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


@app.get("/books", description="Get books with filters",
    response_description="List of books", response_model=List[Book], status_code=200
)
def get_books(name: Optional[str] = Query(default=None)):
    books = load_books()
    if name:
        books = [book for book in books if name.lower() in book.name.lower()]
    return books


@app.post("/books", description="Create a new book",
    response_description="Created book details", response_model=Book, status_code=201
)
def create_book(book: CreateBook = Body()):
    books = load_books()
    new_book_id = uuid4()
    book = Book(**book.model_dump(), id=new_book_id)
    books.append(book)
    save_books(books)
    return book


@app.put("/books/{book_id}", description="Update an existing book by ID",
    response_description="Updated book details", response_model=Book, status_code=200
)
def update_book(book_id: UUID = Path(), updated_book: UpdateBook = Body()):
    books = load_books()
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = Book(**updated_book.model_dump(), id=book_id)
            save_books(books)
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", description="Delete a book by ID",
    response_description="Deletion confirmation", response_model=SuccessMessage, status_code=200
)
def delete_book(book_id: UUID = Path()):
    books = load_books()
    for index, book in enumerate(books):
        if book.id == book_id:
            del books[index]
            save_books(books)
            return SuccessMessage(message="Book was successfully deleted")
    raise HTTPException(status_code=404, detail="Book not found")
