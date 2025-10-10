import pandas as pd

# Fungsi untuk membaca data buku
def load_books_data():
    dataset_path = "C:/Users/akbar1/Downloads/data library management/library_dataset_random.csv"
    return pd.read_csv(dataset_path)

# Fungsi untuk menyimpan data buku
def save_books_data(data):
    dataset_path = "C:/Users/akbar1/Downloads/data library management/library_dataset_random.csv"
    data.to_csv(dataset_path, index=False)
