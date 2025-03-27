import random
from src.translation.translation import _
from src.murderer_generator.murderer_generator import assign_murderer_type, Ritualistic, Possessed, Avenger, Accidental
from src.accomplice_generator.accomlice_generator import assign_accomplice_type, Accomplice
from src.helper_generator.helper_generator import assign_helper_type, Helper
from src.utils.utils import get_data
from src.abstract_npc.abstract_npc import AbstractNpc, npc_data

available_male_names = get_data('male_names', 'npc')
available_female_names = get_data('female_names', 'npc')

def assign_unique_name(available_names):
    name = random.choice(available_names)
    if len(available_names) > 1:
        available_names.remove(name)
    return _(name)

class Person(AbstractNpc):
    used_names = set()  # To track assigned names

    def __init__(self, data, is_new=True):
        super().__init__(npc_data=data, is_new=True)
        if is_new:
            self.role = _(get_data('roles', 'npc')[data['npc_id']])
            self.location = f"{get_data('roles', 'npc')[data['npc_id']]}"
            self.avatar = f"{self.location}.png"
            self.gender = _('Female') if get_data('roles', 'npc')[data['npc_id']] in get_data('female_roles', 'npc') else _(
                'Male')
            self.personalities = []
            self.pressure_response = [_(random.choice(get_data('pressure_response', 'npc')))]
            if self.gender == _('Female'):
                self.name = assign_unique_name(available_female_names)
                self.personalities = []
                self.personalities.append(_('Lover'))
                self.pressure_response.append(_('flirt'))
            else:
                self.name = assign_unique_name(available_male_names)
            race = _('Vampire') if self.role == _('Wanderer') else random.choice(get_data('races', 'npc'))
            self.race = _(race) if get_data('roles', 'npc')[data['npc_id']] in get_data('non_humans', 'npc') else _('Human')
            self.personalities.append(_(random.choice(get_data('personalities', 'npc'))))

            self.alibi = 'Unknown'
            self.connections = {}
            self.suspect = False
            self.known_clues = []

    def get_clues(self, pressure_method):
        """Определяет, какие улики NPC готов раскрыть в зависимости от метода давления."""

        if 'Strong-willed' in self.personalities and pressure_method in ['Threats', 'Blackmail']:
            return "Я не поддамся давлению!"
        elif 'Cowardly' in self.personalities and pressure_method in ['Threats', 'Blackmail']:
            return f'Ладно, ладно! Я скажу... {random.choice(self.known_clues)}'
        elif 'Greedy' in self.personalities and pressure_method == 'Bribery':
            return f'Может, это освежит мою память... {random.choice(self.known_clues)}'
        elif 'Cunning' in self.personalities and pressure_method == 'Blackmail':
            return f'Ты хорошо подготовился... Ладно, вот что я знаю: {random.choice(self.known_clues)}'
        elif 'Straightforward' in self.personalities and pressure_method == 'Persuasion':
            return f"'Я скажу всё как есть: {', '.join(self.known_clues)}'"
        elif 'Silent' in self.personalities:
            return 'NPC молчит и отказывается говорить.'
        elif 'Possessed' in self.personalities:
            return 'NPC ведёт себя странно и бормочет что-то бессвязное...'
        else:
            return 'Я ничего не знаю...'

    def __repr__(self):
        return str({
            'name': self.name,
            'role': self.role,
            'race': self.race,
            'personalities': self.personalities,
            'pressure_response': self.pressure_response,
            'connections': self.connections,
            'known_clues': self.known_clues
        })

npc_list = []

def generate_npc() -> None:
    global npc_list
    npc_list = [Person(data={'is_new': True, 'npc_id': i}) for i in range(len(get_data('roles', 'npc')))]
    assign_relationships(npc_list)

def generate_loaded_npc(loaded_npc_list) -> None:
    global npc_list
    npc_list = []
    for npc in loaded_npc_list:
        if npc['person_type'] == 'Citizen':
            npc_list.append(Person(npc, False))
        if npc['person_type'] == 'Accomplice':
            npc_list.append(Accomplice(npc, False))
        if npc['person_type'] == 'Ritualistic':
            npc_list.append(Ritualistic(npc, False))
        if npc['person_type'] == 'Possessed':
            npc_list.append(Possessed(npc, False))
        if npc['person_type'] == 'Avenger':
            npc_list.append(Avenger(npc, False))
        if npc['person_type'] == 'Accidental':
            npc_list.append(Accidental(npc, False))
        if npc['person_type'] == 'Helper':
            npc_list.append(Helper(npc, False))

    print(npc_list)

def get_npc_list() -> npc_list:
    return npc_list

# Assign relationships
def assign_relationships(npc_list) -> None:
    random.shuffle(npc_list)

    npc_list[0] = assign_murderer_type(npc_list[0].__dict__.copy())
    npc_list[0].set_relationships({'role': 'Murderer'})
    npc_list[1].set_relationships({'role': 'Victim'})

    for npc in npc_list:
        npc.known_clues = npc_list[0].clues['PublicClues']

    # Assign 2 accomplices, 3 helpers, and 2 neutrals
    accomplices = npc_list[2:4]
    helpers = npc_list[4:7]
    neutral_npcs = npc_list[7:]

    # Set connections
    for index, accomplice in enumerate(accomplices):
        accomplice = assign_accomplice_type(accomplice.__dict__.copy(), npc_list[0].__dict__.copy())
        accomplice.set_relationships(
            {
                'role': _('Accomplice'),
                'murderer_name': npc_list[0].name,
                'murderer_role': npc_list[0].role,
                'victim_name': npc_list[1].name,
                'victim_role': npc_list[1].role
            })
        npc_list[index+2] = accomplice
    for index, helper in enumerate(helpers):
        clue = npc_list[0].clues['SecretClues'][index]
        helper = assign_helper_type(helper.__dict__.copy(), clue=clue)
        helper.set_relationships(
            {
                'role': _('Helper'),
                'victim_name': npc_list[1].name,
                'victim_role': npc_list[1].role
            })
        npc_list[index + 4] = helper
    for neutral in neutral_npcs:
        neutral.set_relationships(
            {
                'role': _('Neutral'),
                'victim_name': npc_list[1].name,
                'victim_role': npc_list[1].role
            })

def get_npc(role: str) -> Person or None:
    for npc in npc_list:
        if npc.role == role:
            return npc

    return None

def get_npcs_by_location(location: str) -> Person or None:
    npcs_by_location = []
    for npc in npc_list:
        if npc.location == location:
            npcs_by_location.append(npc)

    return npcs_by_location

def update_npc(npc, relationship_change):
    """Обновляет данные NPC после диалога."""
    npc.update_relationship(relationship_change)