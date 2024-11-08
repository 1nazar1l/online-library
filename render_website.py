from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell

def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html']),
    )

    with open("library/books_dict.json", "r", encoding='utf-8') as my_file:
        books = json.load(my_file)
    
    books = books[:10]

    template = env.get_template('template.html')
    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)



on_reload()
server = Server()
server.watch("template.html", on_reload)
server.serve(root='.')
