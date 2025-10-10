from fastapi import APIRouter, HTTPException
from modules.library.services import ReportService
from typing import List

router = APIRouter()

# Reports for Active and Overdue Loans
@router.get("/reports/active/", response_model=List[str])
def get_active_loans():
    active_loans = ReportService.get_active_loans()
    return active_loans

@router.get("/reports/overdue/", response_model=List[str])
def get_overdue_loans():
    overdue_loans = ReportService.get_overdue_loans()
    return overdue_loans


