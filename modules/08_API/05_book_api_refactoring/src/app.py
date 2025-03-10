from fastapi import FastAPI, Query, Body, HTTPException, Path
from typing import List, Optional
from uuid import uuid4, UUID
from .schemas import Book, UpdateBook, CreateBook, SuccessMessage
from .utils import load_books, save_books


app = FastAPI()


@app.get("/books", description="Get books with filters",
    response_description="List of books", response_model=List[Book], status_code=200
)
async def get_books(name: Optional[str] = Query(default=None)):
    books = await load_books()
    if name:
        books = [book for book in books if name.lower() in book.name.lower()]
    return books


@app.post("/books", description="Create a new book",
    response_description="Created book details", response_model=Book, status_code=201
)
async def create_book(book: CreateBook = Body()):
    books = await load_books()
    new_book_id = uuid4()
    book = Book(**book.model_dump(), id=new_book_id)
    books.append(book)
    await save_books(books)
    return book


@app.put("/books/{book_id}", description="Update an existing book by ID",
    response_description="Updated book details", response_model=Book, status_code=200
)
async def update_book(book_id: UUID = Path(), updated_book: UpdateBook = Body()):
    books = await load_books()
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = Book(**updated_book.model_dump(), id=book_id)
            await save_books(books)
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", description="Delete a book by ID",
    response_description="Deletion confirmation", response_model=SuccessMessage, status_code=200
)
async def delete_book(book_id: UUID = Path()):
    books = await load_books()
    for index, book in enumerate(books):
        if book.id == book_id:
            del books[index]
            await save_books(books)
            return SuccessMessage(message="Book was successfully deleted")
    raise HTTPException(status_code=404, detail="Book not found")
