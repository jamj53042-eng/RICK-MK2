import json, os

class Memory:
    def __init__(self, filename="rick_memory.json"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"level": 1, "xp": 0, "badges": [], "perks": []}
            self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
