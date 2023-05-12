import os
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


def download_comments(comments, book_id, folder='comments/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(f'{folder}{book_id}_comments.txt', 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + '\n')


def download_txt(url, filename, folder):
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


def check_txt_exists(filename, folder):
    file = os.path.join(folder, filename + '.txt')
    return os.path.isfile(file)


def check_img_exists(url, folder):
    unquoted_url = unquote(url)
    path = urlparse(unquoted_url).path
    filename = path.rstrip("/").split("/")[-1]
    file = os.path.join(folder, filename)
    return os.path.isfile(file)


def get_book(book_id):
    img_folder = 'images/'
    book_folder = 'books/'
    download_url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(download_url)
    response.raise_for_status()
    try:
        check_for_redirect(response)

        book = parse_book_page(book_id)
        book_title = book['title']
        img_url = book['img']
        comments = book['comments']
        genres = book['genres']
        author = book['author']
        filename = f'{book_id}. {book_title}'
        if not check_txt_exists(filename, book_folder):
            download_txt(download_url, filename, book_folder)
        if not check_img_exists(img_url, img_folder):
            download_image(img_url, img_folder)
        if comments:
            download_comments(comments, book_id)

        return book_title, genres, author

    except HTTPError as e:
        print(e)


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find(id='content').find('h1').text
    title = title_tag.split('::')[0].strip()

    author = title_tag.split('::')[1].strip()

    img_url_tag = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(url, img_url_tag)

    comments_tags = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments_tags]

    genre_tags = soup.find(id='content').find('span', class_='d_book').find_all('a')
    genres = list(genre.text for genre in genre_tags)

    book_info = {'title': title, 'comments': comments,
                 'genres': genres, 'img': img_url, 'author': author}

    return book_info


def print_book_info(book_id):
    book_title, genres, author = get_book(book_id)
    print(f'Название: {book_title}',
          f'Автор: {author}',
          f'Жанр: {genres}',
          sep='\n', end='\n\n')


def main():
    parser = argparse.ArgumentParser(description='Загружает книги с сайта https://tululu.org')
    parser.add_argument('start_id', type=int,
                        help='Стартовый id книги')
    parser.add_argument('end_id', type=int,
                        help='Конечный id книги')
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            print_book_info(book_id)
        except ValueError:
            print(f'Книга c id {book_id} не найдена', end='\n\n')


if __name__ == '__main__':
    main()
