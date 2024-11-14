from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
import os
from more_itertools import chunked
import math


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html']),
    )

    with open("library/books_dict.json", "r", encoding='utf-8') as my_file:
        books = json.load(my_file)

    os.makedirs("pages", exist_ok=True)

    pages = math.ceil(len(books)/10)

    books = list(chunked(books, 10))
    for i, books_on_page in enumerate(books, 1):

        template = env.get_template('template.html')
        rendered_page = template.render(books=books_on_page, pages=pages, page_number=i)

        with open(f'pages/index{i}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)



on_reload()
server = Server()
server.watch("template.html", on_reload)
server.serve(root='.')
