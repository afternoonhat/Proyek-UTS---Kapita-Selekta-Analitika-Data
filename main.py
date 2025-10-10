from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from datetime import datetime

# Load the dataset into memory
dataset_path = "C:/Users/akbar1/Downloads/data library management/library_dataset_random.csv"
data = pd.read_csv(dataset_path)

# Initialize FastAPI app
app = FastAPI()

# Pydantic model to structure the book data
class Book(BaseModel):
    Book_ID: str
    Title: str
    Author: str
    Category: str
    Cabinet: int
    Rack: int
    Row: int
    Signal_Strength: float
    Timestamp: datetime
    Status: str

# Pydantic model to structure the loan data
class Loan(BaseModel):
    Loan_ID: str
    Book_ID: str
    User_ID: str
    Borrow_Date: datetime
    Return_Date: datetime
    Status: str  # "Active", "Overdue", "Returned"

# Helper function to get the current list of books and loans
def get_books_df():
    return data

# Data for loans (a simple list or DataFrame)
loans_data = pd.DataFrame(columns=["Loan_ID", "Book_ID", "User_ID", "Borrow_Date", "Return_Date", "Status"])


# CRUD for books (already defined in books.py)
@app.get("/books/", response_model=List[Book])
def get_books():
    """ Get list of all books """
    books = get_books_df().to_dict(orient="records")
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: str):
    """ Get details of a single book by Book_ID """
    book = data[data['Book_ID'] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.iloc[0].to_dict()

@app.post("/books/")  # Add book to the library
def add_book(book: Book):
    """ Add a new book to the library """
    new_book = pd.DataFrame([book.dict()])
    global data
    data = pd.concat([data, new_book], ignore_index=True)
    data.to_csv(dataset_path, index=False)  # Save updated data
    return {"message": "Book added successfully", "book_id": book.Book_ID}

@app.put("/books/{book_id}")  # Update a book's details
def update_book(book_id: str, book: Book):
    """ Update details of an existing book """
    idx = data[data['Book_ID'] == book_id].index
    if idx.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for col in book.dict().keys():
        data.loc[idx, col] = book.dict()[col]
    data.to_csv(dataset_path, index=False)  # Save updated data
    return {"message": "Book updated successfully", "book_id": book_id}

@app.delete("/books/{book_id}")  # Delete a book from the library
def delete_book(book_id: str):
    """ Delete a book by Book_ID """
    global data
    data = data[data['Book_ID'] != book_id]
    data.to_csv(dataset_path, index=False)  # Save updated data
    return {"message": "Book deleted successfully", "book_id": book_id}

# CRUD for loans (Student Operations)
@app.post("/loans/")
def borrow_book(loan: Loan):
    """ Borrow a book from the library """
    global loans_data
    new_loan = pd.DataFrame([loan.dict()])
    loans_data = pd.concat([loans_data, new_loan], ignore_index=True)
    return {"message": "Book borrowed successfully", "loan_id": loan.Loan_ID}

@app.get("/loans/", response_model=List[Loan])
def get_loans():
    """ Get list of all loans """
    return loans_data.to_dict(orient="records")

@app.get("/loans/{loan_id}", response_model=Loan)
def get_loan(loan_id: str):
    """ Get details of a single loan by Loan_ID """
    loan = loans_data[loans_data['Loan_ID'] == loan_id]
    if loan.empty:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan.iloc[0].to_dict()

@app.put("/loans/{loan_id}")
def extend_loan(loan_id: str):
    """ Extend the loan period """
    global loans_data
    loan = loans_data[loans_data['Loan_ID'] == loan_id]
    if loan.empty:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Extend return date (example, add 7 days to current return date)
    loans_data.loc[loans_data['Loan_ID'] == loan_id, 'Return_Date'] = pd.to_datetime(loan['Return_Date'].values[0]) + pd.Timedelta(days=7)
    return {"message": "Loan extended successfully"}

@app.put("/loans/return/{loan_id}")
def return_book(loan_id: str):
    """ Return a borrowed book """
    global loans_data
    loan = loans_data[loans_data['Loan_ID'] == loan_id]
    if loan.empty:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Mark the loan as returned
    loans_data.loc[loans_data['Loan_ID'] == loan_id, 'Status'] = 'Returned'
    return {"message": "Book returned successfully"}

# Main entry to run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
