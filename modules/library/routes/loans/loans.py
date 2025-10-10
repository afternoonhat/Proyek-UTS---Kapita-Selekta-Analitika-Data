from fastapi import APIRouter, HTTPException
from modules.library.schema import Loan
from modules.library.services import LoanService
from typing import List

router = APIRouter()


# CRUD for loans (Student Operations)
@router.post("/loans/")
def borrow_book(loan: Loan):
    result = LoanService.borrow_book(loan)
    if not result:
        raise HTTPException(status_code=400, detail="Error borrowing book")
    return {"message": "Book borrowed successfully", "loan_id": loan.Loan_ID}

@router.put("/loans/{loan_id}")
def extend_loan(loan_id: str):
    result = LoanService.extend_loan(loan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Loan extended successfully"}

@router.put("/loans/return/{loan_id}")
def return_book(loan_id: str):
    result = LoanService.return_book(loan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Book returned successfully"}