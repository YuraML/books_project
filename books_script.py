import requests
import os
import argparse
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
from pathlib import Path


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет скачивать книги напрямую с сайта https://tululu.org/')
    parser.add_argument('start_id', help='укажите id первой скачиваемой книги', type=int, default=20)
    parser.add_argument('end_id', help='укажите id последней скачиваемой книги', type=int, default=30)
    return parser


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_title(soup, response):
    check_for_redirect(response)
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_title = title_text.split('::')
    return book_title


def get_image_link(response, soup, book_site_page_url):
    check_for_redirect(response)
    book_image = soup.find('div', class_='bookimage').find('img')['src']
    book_image_link = urljoin(book_site_page_url, book_image)
    return book_image_link


def get_image_id(response, soup, book_site_page_url):
    book_image_link = get_image_link(response, soup, book_site_page_url)
    image_id = unquote(urlparse(book_image_link).path.split('/')[-1])
    image_id = sanitize_filename(image_id)
    return image_id


def download_image(response, soup, book_site_page_url, folder='images/'):
    book_image_link = get_image_link(response, soup, book_site_page_url)
    image_filename = get_image_id(response, soup, book_site_page_url)
    Path("images").mkdir(parents=True, exist_ok=True)
    image_path = os.path.join(folder, image_filename)
    response = requests.get(book_image_link)
    response.raise_for_status()
    with open(image_path, 'wb') as file:
        file.write(response.content)


def get_book_path(response, soup, folder='books/'):
    filename = sanitize_filename(get_book_title(soup, response)[0])
    book_filename = f'{filename.strip()}.txt'
    book_path = os.path.join(folder, book_filename)
    return book_path


def download_txt(response, soup, book_download_url):
    book_path = get_book_path(response, soup, folder='books/')
    Path("books").mkdir(parents=True, exist_ok=True)
    response = requests.get(book_download_url)
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


def parse_book_page(response, soup, book_site_page_url):
    book_page = {
        'book_name': get_book_title(soup, response)[0].strip(),
        'author': get_book_title(soup, response)[1].strip(),
        'book_path': get_book_path(response, soup, folder='books/'),
        'book_image_link': get_image_link(response, soup, book_site_page_url),
        'book_image_id': get_image_id(response, soup, book_site_page_url),
        'comments': get_comments(soup),
        'genres': get_genres(soup)
    }
    print(f'Название: {book_page["book_name"]}', f'Автор: {book_page["author"]}', sep='\n', end='\n')


def main():
    parser = create_parser()
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id + 1):
        book_download_url = f'https://tululu.org/txt.php?id={book_id}'
        book_site_page_url = f'https://tululu.org/b{book_id}/'
        response = requests.get(book_site_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            parse_book_page(response, soup, book_site_page_url)
        except requests.exceptions.HTTPError:
            pass


if __name__ == '__main__':
    main()