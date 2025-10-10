from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Model untuk Buku
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

# Model untuk Peminjaman
class Loan(BaseModel):
    Loan_ID: str
    Book_ID: str
    User_ID: str
    Borrow_Date: datetime
    Return_Date: Optional[datetime] = None
    Status: str  # "Active", "Overdue", etc.
