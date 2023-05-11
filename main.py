import requests
from random import sample

from pathlib import Path


def save_book(response):
        encoding = response.headers['Content-Type'].split('=')[-1].strip('"')
        book_title = response.headers['Content-Disposition'].split('=')[-1].strip('"')
        path = "./books/"
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(f'{path}{book_title}', 'w', encoding=encoding) as file:
            file.write(response.text)
        return 1


def get_book(url):
    # url = 'https://tululu.org/txt.php?id=32168'
    response = requests.get(url)
    response.raise_for_status()
    print(response.headers, response.url, sep='\n')
    if 'txt' in response.url:
        return save_book(response)
    else:
        return 0



def get_10_books():
    url_template = 'https://tululu.org/txt.php?id={}'
    counter = 0
    for i in sample(range(1, 83000), 100):
        counter += get_book(url_template.format(i))
        if counter == 10:
            break

get_10_books()