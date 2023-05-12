from os.path import splitext

import requests
import os

from random import sample
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from requests import HTTPError
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def save_book(response):
    encoding = response.headers['Content-Type'].split('=')[-1].strip('"')
    book_title = response.headers['Content-Disposition'].split('=')[-1].strip('"')
    path = "./books/"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(f'{path}{book_title}', 'w', encoding=encoding) as file:
        file.write(response.text)
    return 1


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    title = sanitize_filename(filename)
    path = os.path.join(folder, f'{title}.txt')
    with open(path, 'w', encoding='utf8') as file:
        file.write(response.text)
    return path


def download_image(url, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    img = urlparse(unquote(url)).path.rstrip("/").split("/")[-1]
    path = os.path.join(folder, img)
    with open(path, 'wb') as file:
        file.write(response.content)


def check_img_exist(url, folder):
    unquoted_url = unquote(url)
    path = urlparse(unquoted_url).path
    filename = path.rstrip("/").split("/")[-1]
    file = os.path.join(folder, filename)
    return os.path.isfile(file)


def get_book(book_id):
    img_folder = 'images/'
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
        book_title, img_url = get_book_info(book_id)
        filename = f'{book_id}. {book_title}'
        download_txt(url, filename)
        if not check_img_exist(img_url, img_folder):
            download_image(img_url, img_folder)
        return book_title, img_url
    except HTTPError as e:
        return str(e)


def get_book_info(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id='content').find('h1').text
    # author = title_tag.split('::')[1].strip()
    title = title_tag.split('::')[0].strip()
    img_url_tag = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(url, img_url_tag)
    return title, img_url


def main():
    amount = 10
    for book_id in range(1, amount + 1):
        print(get_book(book_id))


if __name__ == '__main__':
    main()
