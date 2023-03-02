from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

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
    books_info = {'image': image, 'author': author, 'title': title}
    books_page.append(books_info)

rendered_page = template.render(books=books_page)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
