# Парсер книг с сайта tululu.org

Код на Python для скачивания книг с сайта [tululu.org](https://tululu.org/). Код скачивает книги, обложки и комментарии
книг в текстовые файлы. Все файлы сохраняются в соответствующие папки. Код использует библиотеки requests, argparse, os,
pathlib, pathvalidate, bs4 и urllib.parse.

### Как установить

Чтобы установить и запустить данный код, необходимо выполнить следующие шаги:

- Установить Python на компьютер, если он еще не установлен. Можно скачать установочный файл на
  официальном [сайте](https://www.python.org/downloads/).

- Скачать код из репозитория. Для этого можно нажать на кнопку "Code" и выбрать "Download ZIP".

- Установить необходимые библиотеки. Для этого можно выполнить команду ```pip install -r requirements.txt``` в командной
  строке, находясь в папке проекта.

- Запустить программу, выполнив команду python ```tululu.py start_id:int end_id:int``` в командной строке, где <
  start_id> и <end_id> - это начальный и конечный id книг, которые нужно скачать.

### Аргументы

<start_id> и <end_id> - это начальный и конечный id книг (целые положительные числа), которые нужно скачать. id найти
можно в адресной строке браузера.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).