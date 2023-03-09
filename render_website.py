import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from pathlib import Path


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs('pages/', exist_ok=True)
    with open("json/books_json", "r", encoding="utf8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)

    books_page = []
    for book in books:
        book_details = {'image': book['book_image_filename'],
                        'author': book['author'],
                        'title': book['book_name'],
                        'text': book['book_path'],
                        'genres': book['genres']
                        }
        books_page.append(book_details)

    books_columns = 2
    chunked_books = list(chunked(books_page, books_columns))
    books_per_column = 5
    chunked_pages = list(chunked(chunked_books, books_per_column))
    pages_amount = len(chunked_pages)

    for page_number, books in enumerate(chunked_pages, 1):
        filename = Path('pages/', f'index{page_number}.html')
        rendered_page = template.render(books=books,
                                        page_number=page_number,
                                        pages_amount=pages_amount
                                        )
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()
