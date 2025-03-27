from src.abstract_npc.abstract_npc import AbstractNpc

class Accomplice(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type = 'Accomplice'
        self.clues = []
        self.murderer = []

    def assign_clues(self, clues):
        """Сообщник знает все улики убийцы."""
        self.clues = clues['SecretClues']

    def assign_murderer_info(self, murderer):
        """Сообщник знает все улики убийцы."""
        self.murderer = murderer

# Function to randomly assign a murderer type
def assign_accomplice_type(npc, murderer) -> Accomplice:
    accomplice = Accomplice(npc)
    accomplice.assign_clues(murderer['clues'])
    accomplice.assign_murderer_info(murderer)

    return accomplice


