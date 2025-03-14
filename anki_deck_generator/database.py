import json
from pathlib import Path
from anki_deck_generator import PATH_IS_NOT_JSON_ERROR, ERRORS


class Database:
    location: Path
    data: dict = {}

    def __init__(self, path: str):
        self.location = Path(path)
        self.data = self._load()

    def _load(self):
        with open(self.location, "r") as file:
            return json.load(file)

    def write(self, key: str, value: any):
        self.data[key] = value

        with open(self.location, "w+") as file:
            file.write(json.dumps(self.data, indent=2))
            return self.data[key]

    def read(self, key: str):
        return self.data.get(key, None)
