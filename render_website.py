import json
import os
import math

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import argparse
from pathvalidate import sanitize_filename
import os


def on_reload():
    parser = argparse.ArgumentParser(description="Парсит скачанные книги")
    parser.add_argument("--dest_folder", type=str, default="media", help="Укажите папку в которую будет сохраняться вся информация")
    args = parser.parse_args()
    root_folder = args.dest_folder

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"]),
    )

    filepath = os.path.join(sanitize_filename(root_folder),"books_dict.json")
    with open(filepath, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    os.makedirs("pages", exist_ok=True)

    books_per_page = 10
    books_in_row = 2
    pages = math.ceil(len(books)/books_per_page)
    books = list(chunked(books, books_per_page))

    for i, books_on_page in enumerate(books, 1):
        books = list(chunked(books_on_page, books_in_row))
        template = env.get_template("template.html")
        rendered_page = template.render(books=books, pages=pages, page_number=i)

        filepath = f"pages/index{i}.html"
        if i == 1: 
            filepath = f"pages/index.html"

        with open(filepath, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="pages/index.html")


if __name__ == "__main__":
    main()
