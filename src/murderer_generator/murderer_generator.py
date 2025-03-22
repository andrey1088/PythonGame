import random
from abc import ABC, abstractmethod
from pyclbr import Class
from src.utils.utils import get_data

class MurdererType(ABC):
    def __init__(self, killer: Class):
        self.killer = killer  # Убийца, связанный с этим типом
        self.clue = self.generate_clue() # Улики, связанные с убийством
        self.method = self.murder_method() # Метод убийства

    @abstractmethod
    def generate_clue(self):
        """Генерирует уникальную улику для данного типа убийцы."""
        pass

    @abstractmethod
    def murder_method(self):
        """Возвращает способ убийства."""
        pass


class Ritualist(MurdererType):
    def generate_clue(self):
        return [get_data('Ritualist', 'clues')]

    def murder_method(self):
        return "The victim was sacrificed in a dark ritual."


class Possessed(MurdererType):
    def generate_clue(self):
        return [get_data('Possessed', 'clues')]

    def murder_method(self):
        return "The murderer was possessed and had no control over their actions."


class Avenger(MurdererType):
    def generate_clue(self):
        return [get_data('Avenger', 'clues')]

    def murder_method(self):
        return "The murderer acted out of revenge."


class AccidentalKiller(MurdererType):
    def generate_clue(self):
        return [get_data('AccidentalKiller', 'clues')]

    def murder_method(self):
        return "The murder happened unintentionally during a conflict."


# Function to randomly assign a murderer type
def assign_murderer_type(npc: Class) -> Class:
    murderer_classes = [Ritualist, Possessed, Avenger, AccidentalKiller]
    return random.choice(murderer_classes)(npc.name)


