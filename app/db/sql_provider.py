from jinja2 import Template
import os

class SQLProvider:
    def __init__(self, folder):
        self.folder = folder

    def get(self, filename, **params):
        path = os.path.join(self.folder, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"SQL-файл не найден: {path}")
        with open(path, encoding='utf-8') as f:
            template = Template(f.read())
        return template.render(**params)
