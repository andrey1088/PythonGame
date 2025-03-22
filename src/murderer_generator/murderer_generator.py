import random
from abc import ABC, abstractmethod
from pyclbr import Class

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
        return [
            "Symbols drawn in blood found near the body.",
            "Burnt candles and ritual circles in the victim's house.",
            "A torn page from an occult book discovered nearby."
        ]

    def murder_method(self):
        return "The victim was sacrificed in a dark ritual."


class Possessed(MurdererType):
    def generate_clue(self):
        return [
            "Witnesses claim the murderer spoke in an unnatural voice.",
            "Strange scratches on the walls, as if made by something inhuman.",
            "The murderer has no recollection of the crime."
        ]

    def murder_method(self):
        return "The murderer was possessed and had no control over their actions."


class Avenger(MurdererType):
    def generate_clue(self):
        return [
            "A letter was found near the body, detailing a grudge.",
            "The victim and murderer were known to have had conflicts.",
            "A missing weapon from the murderer's home matches the wound."
        ]

    def murder_method(self):
        return "The murderer acted out of revenge."


class AccidentalKiller(MurdererType):
    def generate_clue(self):
        return [
            "Unusual bruises suggest a struggle rather than a planned murder.",
            "A broken chair and shattered glass near the body indicate a fight.",
            "Footprints leading away from the scene suggest someone fled in panic."
        ]

    def murder_method(self):
        return "The murder happened unintentionally during a conflict."


# Function to randomly assign a murderer type
def assign_murderer_type(npc: Class) -> Class:
    murderer_classes = [Ritualist, Possessed, Avenger, AccidentalKiller]
    return random.choice(murderer_classes)(npc.name)


