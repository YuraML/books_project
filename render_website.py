from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open("json/books_json", "r", encoding="utf8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)
    books_page = []
    for book in books:
        image = book['book_image_link']
        author = book['author']
        title = book['book_name']
        text = book['book_path']
        books_info = {'image': image, 'author': author, 'title': title, 'text': text}
        books_page.append(books_info)

    chunked_books = list(chunked(books_page, 2))
    rendered_page = template.render(books=chunked_books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
