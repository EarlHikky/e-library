import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('main').find('header').find('h1')
    title_text = title_tag.text
    print(title_text)
    img = soup.find('img', class_='attachment-post-image')['src']
    print(img)
    print()
    post_text = soup.find('div', class_="entry-content").text
    print(post_text)


if __name__ == '__main__':
    main()
