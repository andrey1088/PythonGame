class AbstractNpc:
    def __init__(self):
        self.id = ''
        self.role = ''
        self.gender = ''
        self.personalities = []
        self.pressure_response = []
        self.murderer_info = None
        self.accomplice_info = None
        self.helper_info = None
        self.name = ''
        self.personalities = []
        self.race = ''
        self.alibi = ''
        self.connections = {}
        self.suspect = False
        self.known_clues = []