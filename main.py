import os
import time

import requests
import argparse

from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from requests import HTTPError
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_comments_from_tululu_for_book(comments, path, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(f'{comment}\n')


def download_txt(response, path, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf8') as file:
        file.write(response.text)


def download_image(url, path, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_book(book_id):
    img_folder = 'images/'
    book_folder = 'books/'
    comments_folder = 'comments/'

    params = {'id': book_id}
    url = f'https://tululu.org/txt.php'
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    book = get_book_info_page(book_id)
    book_title = book['title']
    img_url = book['img']
    comments = book['comments']

    book_txt_title = sanitize_filename(f'{book_id}. {book_title}.txt')
    book_txt_path = os.path.join(book_folder, book_txt_title)

    img_title = urlparse(unquote(img_url)).path.rstrip("/").split("/")[-1]
    img_path = os.path.join(img_folder, img_title)

    comments_file_title = f'{book_id}_comments.txt'
    comments_path = os.path.join(comments_folder, comments_file_title)

    if not os.path.isfile(book_txt_path):
        download_txt(response, book_txt_path, book_folder)
    if not os.path.isfile(img_path) and img_url:
        download_image(img_url, img_path, img_folder)
    if not os.path.isfile(comments_path) and comments:
        download_comments_from_tululu_for_book(comments, comments_path, comments_folder)


def get_book_info_page(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)    
    response.raise_for_status()
    return parse_book_page(response)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('div', id='content').find('h1').text
    title = title_tag.split('::')[0].strip()

    author = title_tag.split('::')[1].strip()

    img_url_tag = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(response.url, img_url_tag)

    comments_tags = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments_tags]

    genre_tags = soup.find('div', id='content').find('span', class_='d_book').find_all('a')
    genres = list(genre.text for genre in genre_tags)

    book = {'title': title, 'comments': comments,
            'genres': genres, 'img': img_url, 'author': author}

    return book


def main():
    parser = argparse.ArgumentParser(description='Загружает книги с сайта https://tululu.org')
    parser.add_argument('start_id', type=int,
                        help='Стартовый id')
    parser.add_argument('end_id', type=int,
                        help='Конечный id')
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            get_book(book_id)
        except HTTPError:
            print(f'Книга c id {book_id} не найдена')
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    main()
