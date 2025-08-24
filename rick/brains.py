
class RickBrains:
    def __init__(self, memory=None, say=None):
        self.memory = memory or {}
        self.say = say or print

    def think(self, text):
        return f"Rick thinks: {text}"
