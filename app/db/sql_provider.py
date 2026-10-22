from pathlib import Path

class SQLProvider:
    def __init__(self, folder):
        self.scripts = {
            file.name: file.read_text(encoding="utf-8")
            for file in Path(folder).iterdir()
            if file.is_file() and file.suffix == ".sql"
        }

    def get(self, filename):
        return self.scripts[filename]
