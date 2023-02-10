import requests
import os

os.makedirs("C:/Users/malas/PycharmProjects/books_project/Books", exist_ok=True)
for book_id in range(1, 11):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    filename = f'id{book_id}'
    with open(f"C:/Users/malas/PycharmProjects/books_project/Books/{filename}", 'w', encoding="CP1251") as file:
        file.write(response.text)
