import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from books_script import download_txt, download_image, parse_book_page, check_for_redirect
import json
from time import sleep
import argparse
import os


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет скачивать книги с раздела научной фантастики с сайта https://tululu.org/')
    parser.add_argument('--start_page', help='Укажите с какой страницы раздела начать скачивание', type=int, default=1)
    parser.add_argument('--end_page', help='Укажите до какой страницы продолжать скачивание', type=int, default=702)
    parser.add_argument('--dest_folder',
                        help='Укажите путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('--skip_imgs', help='Не скачивать картинки', action='store_true')
    parser.add_argument('--skip_txt', help='Не скачивать книги', action='store_true')
    parser.add_argument('--json_path', help='Укажите свой путь к *.json файлу с результатами', default='json')
    return parser


def main():
    books_description = []
    reconnect_time = 60
    parser = create_parser()
    args = parser.parse_args()
    dest_folder = args.dest_folder
    os.chdir(dest_folder) if dest_folder else None
    json_path = args.json_path
    os.makedirs(json_path, exist_ok=True)

    for books_page in range(args.start_page, args.end_page):
        book_url = 'https://tululu.org/b'
        book_download_url = 'https://tululu.org/txt.php'
        books_page_url = f'https://tululu.org/l55/{books_page}/'
        books_page_response = requests.get(books_page_url)
        soup = BeautifulSoup(books_page_response.text, 'lxml')
        books_page_selector = 'table.d_book'
        books_on_page = soup.select(books_page_selector)

        for book in books_on_page:
            try:
                book_full_id = book.select_one('a')['href']
                book_link = urljoin(book_url, book_full_id)
                book_id = book_full_id.replace('/', '')[1:]
                book_site_page_url = f'https://tululu.org/b{book_id}/'
                response = requests.get(book_site_page_url)
                response.raise_for_status()
                check_for_redirect(response)
                book_page = parse_book_page(response, book_link)
                book_path, image_filename, book_image_link = book_page["book_path"], book_page['book_image_filename'], \
                    book_page['book_image_link']

                if not args.skip_txt:
                    download_txt(book_path, book_download_url, book_id)
                elif not args.skip_imgs:
                    download_image(image_filename, book_image_link)
                books_description.append(book_page)

            except (requests.exceptions.HTTPError, AttributeError):
                logging.warning(f'Книга с id {book_id} не найдена.')
            except requests.exceptions.ConnectionError:
                logging.warning('Соединение прервано, повторное соединение через 60 секунд.')
                sleep(reconnect_time)
                continue
    with open(f'{json_path}/books_json', "w", encoding='utf8') as json_file:
        json.dump(books_description, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
