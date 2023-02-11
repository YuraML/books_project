import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
from pathlib import Path

def check_for_redirect(response):
    if not response.history:
        raise requests.HTTPError


def get_book_name(response2):
    soup = BeautifulSoup(response2.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    header = title_text.split('::')
    return header[0].strip()


def get_image_link(book_site_page_url, book_sitepage_response):
    soup = BeautifulSoup(book_sitepage_response.text, 'lxml')
    book_image = soup.find('div', class_='bookimage').find('img')['src']
    book_image_link = urljoin(book_site_page_url, book_image)
    return book_image_link

def download_image(book_image_link, folder='images/'):
    pic_filename = unquote(urlparse(book_image_link).path.split('/')[-1])
    pic_filename = sanitize_filename(pic_filename)
    Path("images").mkdir(parents=True, exist_ok=True)
    pic_path = os.path.join(folder, pic_filename)
    response = requests.get(book_image_link)
    response.raise_for_status()
    with open(pic_path, 'wb') as file:
        file.write(response.content)



def download_txt(filename, folder='books/'):
    book_filename = f'{sanitize_filename(filename)}.txt'
    book_path = os.path.join(folder, book_filename)
    return book_path


for book_id in range(5, 10):
    book_download_url = f'https://tululu.org/txt.php?id={book_id}'
    book_site_page_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_download_url)
    response.raise_for_status()
    book_sitepage_response = requests.get(book_site_page_url)
    book_sitepage_response.raise_for_status()
    filename = get_book_name(book_sitepage_response)
    book_image_link = get_image_link(book_site_page_url, book_sitepage_response)
    download_image(book_image_link, folder='images/')
