import random
from abc import ABC, abstractmethod
from pyclbr import Class

class MurdererType(ABC):
    def __init__(self, killer: Class):
        self.killer = killer  # Убийца, связанный с этим типом
        self.clue = self.generate_clue()  # Улика, связанная с убийством

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
        return "Symbols drawn in blood found near the body."

    def murder_method(self):
        return "The victim was sacrificed in a dark ritual."


class Possessed(MurdererType):
    def generate_clue(self):
        return "Witnesses claim the murderer spoke in an unnatural voice."

    def murder_method(self):
        return "The murderer was possessed and had no control over their actions."


class Avenger(MurdererType):
    def generate_clue(self):
        return "A letter was found near the body, detailing a grudge."

    def murder_method(self):
        return "The murderer acted out of revenge."


class AccidentalKiller(MurdererType):
    def generate_clue(self):
        return "Unusual bruises suggest a struggle rather than a planned murder."

    def murder_method(self):
        return "The murder happened unintentionally during a conflict."


# Function to randomly assign a murderer type
def assign_murderer_type(npc: Class) -> Class:
    murderer_classes = [Ritualist, Possessed, Avenger, AccidentalKiller]
    return random.choice(murderer_classes)(npc.name)


