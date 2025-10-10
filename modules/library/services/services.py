import pandas as pd
from datetime import datetime
from modules.library.storage import save_books_data, repository

# Load initial data
books_data = repository.load_books_data()
loans_data = pd.DataFrame()  # Will be used to track loans

# Service untuk Buku
class BookService:
    @staticmethod
    def get_books():
        return books_data.to_dict(orient="records")
    
    @staticmethod
    def get_book(book_id: str):
        book = books_data[books_data['Book_ID'] == book_id]
        if not book.empty:
            return book.iloc[0].to_dict()
        return None

    @staticmethod
    def add_book(book_data):
        global books_data
        new_book = pd.DataFrame([book_data.dict()])
        books_data = pd.concat([books_data, new_book], ignore_index=True)
        repository.save_books_data(books_data)  # Save updated data
        return True

    @staticmethod
    def update_book(book_id: str, book_data):
        global books_data
        idx = books_data[books_data['Book_ID'] == book_id].index
        if idx.empty:
            return False
        for col in book_data.dict().keys():
            books_data.loc[idx, col] = book_data.dict()[col]
        repository.save_books_data(books_data)  # Save updated data
        return True

    @staticmethod
    def delete_book(book_id: str):
        global books_data
        books_data = books_data[books_data['Book_ID'] != book_id]
        repository.save_books_data(books_data)  # Save updated data
        return True

# Service untuk Peminjaman

class LoanService:
    @staticmethod
    def borrow_book(loan_data):
        global loans_data
        # Cek apakah buku masih tersedia
        book = loans_data[loans_data['Book_ID'] == loan_data.Book_ID]
        if book.empty:
            return False  # Buku tidak ditemukan
        # Tambahkan pinjaman baru
        new_loan = pd.DataFrame([loan_data.dict()])
        loans_data = pd.concat([loans_data, new_loan], ignore_index=True)
        save_books_data(loans_data)  # Simpan data pinjaman yang baru
        return True

    @staticmethod
    def extend_loan(loan_id):
        global loans_data
        # Periksa apakah loan_id ada
        loan = loans_data[loans_data['Loan_ID'] == loan_id]
        if loan.empty:
            return False
        # Perpanjang pinjaman (misalnya, tambah tanggal pengembalian)
        loans_data.loc[loans_data['Loan_ID'] == loan_id, 'Return_Date'] = pd.Timestamp.now() + pd.Timedelta(days=7)  # Tambah 7 hari
        save_books_data(loans_data)  # Simpan perubahan
        return True

    @staticmethod
    def return_book(loan_id):
        global loans_data
        # Periksa apakah loan_id ada
        loan = loans_data[loans_data['Loan_ID'] == loan_id]
        if loan.empty:
            return False
        # Tandai pinjaman sebagai dikembalikan
        loans_data.loc[loans_data['Loan_ID'] == loan_id, 'Status'] = 'Returned'
        save_books_data(loans_data)  # Simpan perubahan
        return True

# Service untuk Laporan
class ReportService:
    @staticmethod
    def get_active_loans():
        return loans_data[loans_data['Status'] == 'Active'].to_dict(orient="records")

    @staticmethod
    def get_overdue_loans():
        return loans_data[loans_data['Status'] == 'Overdue'].to_dict(orient="records")
