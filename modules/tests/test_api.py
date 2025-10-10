from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_add_book():
    new_book = {
        "Book_ID": "B999",
        "Title": "Test Book",
        "Author": "Test Author",
        "Category": "Test Category",
        "Cabinet": 1,
        "Rack": 2,
        "Row": 3,
        "Signal_Strength": -45,
        "Timestamp": "2025-01-01T00:00:00",
        "Status": "Present"
    }
    response = client.post("/books/", json=new_book)
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"
