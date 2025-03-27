from src.abstract_npc.abstract_npc import AbstractNpc

class Helper(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type = 'Helper'
        self.clues = []

    def assign_clues(self, clue):
        """Сообщник знает все улики убийцы."""
        self.clues.append(clue)

# Function to randomly assign a murderer type
def assign_helper_type(npc, clue: str) -> Helper:
    helper = Helper(npc)
    helper.assign_clues(clue)

    return helper


