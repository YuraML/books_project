import argparse
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

    parser = argparse.ArgumentParser(
        description='Скрипт позволяет запустить сайт с библиотекой книг научной фантастики.')
    parser.add_argument('--json_path', help='Укажите путь к файлу json.', default="books.json")
    args = parser.parse_args()
    json_path = args.json_path
    with open(json_path, "r", encoding="utf8") as file:
        book_descriptions = json.load(file)

    chunked_book_cards = list(chunked(book_descriptions, 2))
    book_cards_per_column = 5
    chunked_pages = list(chunked(chunked_book_cards, book_cards_per_column))
    pages_amount = len(chunked_pages)

    for page_number, book_cards in enumerate(chunked_pages, 1):
        page_path = Path('pages/', f'index{page_number}.html')
        rendered_page = template.render(book_cards=book_cards,
                                        page_number=page_number,
                                        pages_amount=pages_amount
                                        )
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()
