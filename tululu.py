import requests
import os

from random import sample
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from requests import HTTPError


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


def get_book(book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
        filename = f'{book_id}. {get_book_info(book_id)}'
        download_txt(url, filename)
    except HTTPError as e:
        print(e)


def get_10_books():
    url_template = 'https://tululu.org/txt.php?id={}'
    counter = 0
    for i in sample(range(1, 83000), 100):
        counter += get_book(url_template.format(i))
        if counter == 10:
            break


def get_book_info(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id='content').find('h1').text
    # author = title_tag.split('::')[1].strip()
    title = title_tag.split('::')[0].strip()
    return title


def main():
    for book_id in range(1, 11):
        get_book(book_id)


if __name__ == '__main__':
    main()
