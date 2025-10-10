from fastapi import APIRouter, HTTPException
from modules.library.schema import Book
from modules.library.services import BookService
from typing import List

router = APIRouter()

# CRUD Books for Admin
@router.get("/books/", response_model=List[Book])
def get_books():
    books = BookService.get_books()
    return books

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: str):
    book = BookService.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books/")
def add_book(book: Book):
    result = BookService.add_book(book)
    if not result:
        raise HTTPException(status_code=400, detail="Error adding book")
    return {"message": "Book added successfully", "book_id": book.Book_ID}

@router.put("/books/{book_id}")
def update_book(book_id: str, book: Book):
    result = BookService.update_book(book_id, book)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully"}

@router.delete("/books/{book_id}")
def delete_book(book_id: str):
    result = BookService.delete_book(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
