class Inquisitor:
    def __init__(self, name='Andrey', authority=5):
        self.name = name
        self.collected_clues = []
        self.authority = authority

    def collect_clue(self, clue):
        """Игрок может собирать улики."""
        self.collected_clues.append(clue)

    def update_authority(self, change):
        """Изменяет уровень авторитета."""
        self.authority += change

    def __repr__(self):
        return f"<Inquisitor {self.name}, Collected Clues: {self.collected_clues}>"

inquisitor = Inquisitor()

