import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def get_book_name(response2):
    soup = BeautifulSoup(response2.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    header = title_text.split('::')
    return header[0].strip()


def check_for_redirect(response):
    if not response.history:
        raise requests.exceptions.HTTPError


def download_txt(book_download_url, filename, folder='books/'):
    book_filename = f'{sanitize_filename(filename)}.txt'
    book_path = os.path.join(folder, book_filename)
    return book_path


for book_id in range(1, 11):
    book_download_url = f'https://tululu.org/txt.php?id={book_id}'
    book_site_page_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_download_url)
    response.raise_for_status()
    book_title_response = requests.get(book_site_page_url)
    book_title_response.raise_for_status()
    filename = get_book_name(book_title_response)
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        with open(download_txt(book_download_url, filename, folder='books/'), 'w', encoding="CP1251") as file:
            file.write(response.text)
