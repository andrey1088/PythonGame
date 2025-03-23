from src.abstract_npc.abstract_npc import AbstractNpc

class Helper:
    def __init__(self, npc):
        super().__init__()
        self.name = 'Helper'
        self.clues = []

    def assign_clues(self, clue):
        """Сообщник знает все улики убийцы."""
        self.clues.append(clue)

# Function to randomly assign a murderer type
def assign_helper_type(npc: AbstractNpc, clue: str) -> Helper:
    helper = Helper(npc)
    helper.assign_clues(clue)

    return helper


