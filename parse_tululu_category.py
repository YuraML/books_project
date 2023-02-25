import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from books_script import download_txt, download_image, parse_book_page, check_for_redirect
import json
from time import sleep


def main():
    books_description = []
    reconnect_time = 60
    for books_page in range(1, 5):
        book_url = 'https://tululu.org/b'
        book_download_url = 'https://tululu.org/txt.php'
        books_page_url = f'https://tululu.org/l55/{books_page}/'
        books_page_response = requests.get(books_page_url)
        soup = BeautifulSoup(books_page_response.text, 'lxml')
        books_list = soup.find_all('table', class_='d_book')
        for book in books_list:
            try:
                book_full_id = book.find('a')['href']
                book_link = urljoin(book_url, book_full_id)
                book_id = book_full_id.replace('/', '')[1:]
                book_site_page_url = f'https://tululu.org/b{book_id}/'
                response = requests.get(book_site_page_url)
                response.raise_for_status()
                check_for_redirect(response)
                book_page = parse_book_page(response, book_link)
                book_path, image_filename, book_image_link = book_page['book_path'], book_page['book_image_filename'], \
                    book_page['book_image_link']
                download_txt(book_path, book_download_url, book_id)
                download_image(image_filename, book_image_link)
                books_description.append(book_page)
                print(f'Книга с id {book_id} скачана. Название: {book_page["book_name"]}',
                      f'Автор: {book_page["author"]}')
            except (requests.exceptions.HTTPError, AttributeError):
                logging.warning(f'Книга с id {book_id} не найдена.')
            except requests.exceptions.ConnectionError:
                logging.warning('Соединение прервано, повторное соединение через 60 секунд.')
                sleep(reconnect_time)
                continue
    with open("book_page_json", "w", encoding='utf8') as json_file:
        json.dump(books_description, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
