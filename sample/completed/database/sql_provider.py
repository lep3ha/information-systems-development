import os

class SQLProvider:
    def __init__(self, file_path):
        self.scripts = {}
        self._load_sql_files(file_path)

    def _load_sql_files(self, directory):
        if not os.path.exists(directory):
            raise Exception(f"SQL directory does not exist: {directory}")

        print(f"Loading SQL files from: {directory}")

        for file in os.listdir(directory):
            if file.endswith('.sql'):
                full_path = os.path.join(directory, file)

                print(f"Found SQL file: {file}")

                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        _sql = f.read()
                    self.scripts[file] = _sql
                    print(f"✓ Successfully loaded: {file}")
                except UnicodeDecodeError:
                    try:
                        with open(full_path, 'r', encoding='cp1251') as f:
                            _sql = f.read()
                        self.scripts[file] = _sql
                        print(f"✓ Successfully loaded {file} with cp1251")
                    except Exception as e:
                        print(f"✗ Error loading {file}: {e}")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")

    def get(self, file_name):
        _sql = self.scripts.get(file_name)
        if _sql is None:
            available_files = list(self.scripts.keys())
            raise FileNotFoundError(f"SQL file '{file_name}' not found. Available files: {available_files}")
        return _sql