import requests
import os
import argparse
import logging
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
from pathlib import Path
from time import sleep


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет скачивать книги напрямую с сайта https://tululu.org/')
    parser.add_argument('start_id', help='укажите id первой скачиваемой книги', type=int, default=20)
    parser.add_argument('end_id', help='укажите id последней скачиваемой книги', type=int, default=30)
    return parser


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_title(soup):
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_title = title_text.split('::')
    return book_title


def get_image_link(soup, book_site_page_url):
    book_image = soup.find('div', class_='bookimage').find('img')['src']
    book_image_link = urljoin(book_site_page_url, book_image)
    return book_image_link


def get_image_filename(book_image_link):
    image_filename = unquote(urlparse(book_image_link).path.split('/')[-1])
    image_filename = sanitize_filename(image_filename)
    return image_filename


def download_image(book_page, folder):
    Path("images").mkdir(parents=True, exist_ok=True)
    image_filename = book_page['book_image_filename']
    book_image_link = book_page['book_image_link']
    image_path = os.path.join(folder, image_filename)
    response = requests.get(book_image_link)
    response.raise_for_status()
    check_for_redirect(response)
    with open(image_path, 'wb') as file:
        file.write(response.content)


def get_book_path(book_title, folder):
    filename = sanitize_filename(book_title[0])
    book_filename = f'{filename.strip()}.txt'
    book_path = os.path.join(folder, book_filename)
    return book_path


def download_txt(book_page, book_download_url, params):
    Path("books").mkdir(parents=True, exist_ok=True)
    book_path = book_page['book_path']
    response = requests.get(book_download_url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open(book_path, 'wb') as file:
        file.write(response.content)


def get_comments(soup):
    comments = soup.find_all('div', class_='texts')
    book_comments = [comment.find('span').text for comment in comments]
    return book_comments


def get_genres(soup):
    genres = soup.find('span', class_='d_book').find_all('a')
    book_genres = [genre.text for genre in genres]
    return book_genres


def parse_book_page(response, book_site_page_url):
    soup = BeautifulSoup(response.text, 'lxml')
    book_title = get_book_title(soup)
    book_path = get_book_path(book_title, folder='books/')
    book_image_link = get_image_link(soup, book_site_page_url)
    image_filename = get_image_filename(book_image_link)
    book_name, book_author = book_title
    book_page = {
        'book_name': book_name.strip(),
        'author': book_author.strip(),
        'book_path': book_path,
        'book_image_link': book_image_link,
        'book_image_filename': image_filename,
        'comments': get_comments(soup),
        'genres': get_genres(soup)
    }
    return book_page


def main():
    logging.basicConfig(level=logging.INFO)
    parser = create_parser()
    args = parser.parse_args()
    reconnect_time = 60
    for book_id in range(args.start_id, args.end_id + 1):
        book_download_url = f'https://tululu.org/'
        book_site_page_url = f'https://tululu.org/b{book_id}/'
        params = {'id': f'txt.php{book_id}'}
        try:
            response = requests.get(book_site_page_url)
            response.raise_for_status()
            check_for_redirect(response)
            book_page = parse_book_page(response, book_site_page_url)
            download_txt(book_page, book_download_url, params)
            download_image(book_page, folder='images/')
            print(f'Книга с id {book_id} скачана. Название: {book_page["book_name"]}', f'Автор: {book_page["author"]}')
        except (requests.exceptions.HTTPError, AttributeError):
            logging.warning(f'Книга с id {book_id} не найдена.')
        except requests.exceptions.ConnectionError:
            logging.warning('Соединение прервано, повторное соединение через 60 секунд.')
            sleep(reconnect_time)
            continue


if __name__ == '__main__':
    main()
