class Inquisitor:
    def __init__(self, name):
        self.name = name
        self.collected_clues = []  # Улики, которые нашёл игрок

    def collect_clue(self, clue):
        """Игрок может собирать улики."""
        self.collected_clues.append(clue)

    def __repr__(self):
        return f"<Inquisitor {self.name}, Collected Clues: {self.collected_clues}>"