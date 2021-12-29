import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

LINES_ON_PAGE = 5
COLUMNS_ON_PAGE = 2


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    with open("books.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    pairs_books = list(chunked(books, COLUMNS_ON_PAGE))
    splited_books = list(chunked(pairs_books, LINES_ON_PAGE))

    os.makedirs('pages', exist_ok=True)

    for page, page_books in enumerate(splited_books, start=1):
        rendered_page = template.render(
            books=page_books,
            total_pages=len(splited_books),
            current_page=page
        )
        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilt")


def main():
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')


if __name__ == "__main__":
    main()
