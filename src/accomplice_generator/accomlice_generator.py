from src.abstract_npc.abstract_npc import AbstractNpc

class Accomplice:
    def __init__(self, npc):
        super().__init__()
        self.name = 'Accomplice'
        self.clues = []
        self.killer = []

    def assign_clues(self, clues):
        """Сообщник знает все улики убийцы."""
        self.clues = clues

    def assign_killer_info(self, killer):
        """Сообщник знает все улики убийцы."""
        self.killer = killer

# Function to randomly assign a murderer type
def assign_accomplice_type(npc: AbstractNpc, killer: AbstractNpc) -> Accomplice:
    accomplice = Accomplice(npc)
    accomplice.assign_clues(killer.murderer_info.clues)
    accomplice.assign_killer_info(killer)

    return accomplice


