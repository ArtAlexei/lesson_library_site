import json, os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    with open("books.json", "r", encoding="utf-8") as file:
        books = json.loads(file.read())

    books = list(chunked(books, 2))

    os.makedirs('pages', exist_ok=True)
    books = list(chunked(books, 5))
    for page, page_books in enumerate(books):
        rendered_page = template.render(
            books=page_books,
            total_pages=len(books),
            current_page=page+1
        )
        with open(f'pages/index{page+1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilt")


rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='.')
