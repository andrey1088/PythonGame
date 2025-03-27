import random
from src.utils.utils import get_data
from src.abstract_npc.abstract_npc import AbstractNpc

class Ritualistic(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type = 'Ritualistic'
        self.clues = self.generate_clue()  # Улики, связанные с убийством
        self.method = self.murder_method()  # Метод убийства

    def generate_clue(self):
        return get_data('Ritualistic', 'clues')

    def murder_method(self):
        return "The victim was sacrificed in a dark ritual."


class Possessed(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type = 'Possessed'
        self.clues = self.generate_clue()
        self.method = self.murder_method()

    def generate_clue(self):
        return get_data('Possessed', 'clues')

    def murder_method(self):
        return "The murderer was possessed and had no control over their actions."


class Avenger(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type='Avenger'
        self.clues = self.generate_clue()  # Улики, связанные с убийством
        self.method = self.murder_method()  # Метод убийства

    def generate_clue(self):
        return get_data('Avenger', 'clues')

    def murder_method(self):
        return "The murderer acted out of revenge."


class Accidental(AbstractNpc):
    def __init__(self, npc, is_new=True):
        super().__init__(npc, is_new)
        self.person_type='Accidental'
        self.clues = self.generate_clue()  # Улики, связанные с убийством
        self.method = self.murder_method()  # Метод убийства

    def generate_clue(self):
        return get_data('Accidental', 'clues')

    def murder_method(self):
        return "The murder happened unintentionally during a conflict."


# Function to randomly assign a murderer type
def assign_murderer_type(npc) -> AbstractNpc:
    murderer_classes = [Ritualistic, Possessed, Avenger, Accidental]
    murderer = random.choice(murderer_classes)(npc)
    return murderer


