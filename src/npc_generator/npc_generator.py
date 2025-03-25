import random
from src.translation.translation import _
from src.murderer_generator.murderer_generator import assign_murderer_type
from src.accomplice_generator.accomlice_generator import assign_accomplice_type
from src.helper_generator.helper_generator import assign_helper_type
from src.utils.utils import get_data
from src.abstract_npc.abstract_npc import AbstractNpc

available_male_names = get_data('male_names', 'npc')
available_female_names = get_data('female_names', 'npc')

def assign_unique_name(available_names):
    name = random.choice(available_names)
    if len(available_names) > 1:
        available_names.remove(name)
    return _(name)

class Person(AbstractNpc):
    used_names = set()  # To track assigned names

    def __init__(self, npc_id):
        super().__init__()
        self.id = npc_id
        self.role = _(get_data('roles', 'npc')[npc_id])
        self.avatar = f"{get_data('roles', 'npc')[npc_id]}.png"
        self.gender = _('Female') if get_data('roles', 'npc')[npc_id] in get_data('female_roles', 'npc') else _('Male')
        self.personalities = []
        self.pressure_response = [_(random.choice(get_data('pressure_response', 'npc')))]
        self.murderer_info = None
        self.accomplice_info = None
        if self.gender == _('Female'):
            self.name = assign_unique_name(available_female_names)
            self.personalities = []
            self.personalities.append(_('Lover'))
            self.pressure_response.append(_('flirt'))
        else:
            self.name = assign_unique_name(available_male_names)
        race = _('Vampire') if self.role == _('Wanderer') else random.choice(get_data('races', 'npc'))
        self.race = _(race) if get_data('roles', 'npc')[npc_id] in get_data('non_humans', 'npc') else _('Human')
        self.personalities.append(_(random.choice(get_data('personalities', 'npc'))))

        self.alibi = 'Unknown'
        self.connections = {}
        self.suspect = False
        self.known_clues = []

    def set_relationships(self, relationships: dict) -> None:
        self.connections = relationships

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

    def update_relationship(self, change):
        """Изменяет отношение NPC к инквизитору."""
        self.relationship_with_inquisitor += change

    def __repr__(self):
        return str({
            'name': self.name,
            'role': self.role,
            'race': self.race,
            'personalities': self.personalities,
            'pressure_response': self.pressure_response,
            'connections': self.connections,
            'murderer_info': self.murderer_info,
            'accomplice_info': self.accomplice_info,
            'known_clues': self.known_clues
        })

# Generate NPCs
npc_list = [Person(i) for i in range(len(get_data('roles', 'npc')))]

# Assign relationships
def assign_relationships() -> None:
    random.shuffle(npc_list)

    # Assign main roles
    main_roles = [_('Victim'), _('Killer')]
    main_npcs = random.sample(npc_list, 2)
    murderer = None
    victim = None

    for i in range(len(main_roles)):
        main_npcs[i].set_relationships({'role': main_roles[i]})
        if main_roles[i] == _('Killer'):
            murderer = main_npcs[i]
            murderer.murderer_info = assign_murderer_type(murderer)
        else:
            victim = main_npcs[i]

    for npc in npc_list:
        npc.known_clues = murderer.murderer_info.clues['PublicClues']

    # Assign 2 accomplices, 3 helpers, and 2 neutrals
    accomplices = random.sample([npc for npc in npc_list if npc not in main_npcs], 2)
    helpers = random.sample([npc for npc in npc_list if npc not in accomplices and npc not in main_npcs], 3)
    neutral_npcs = [npc for npc in npc_list if npc not in accomplices and npc not in helpers and npc not in main_npcs]

    # Set connections
    for accomplice in accomplices:
        accomplice.set_relationships(
            {
                'role': _('Accomplice'),
                'knows_about': [murderer.name],
                'victim_name': victim.name,
                'victim_role': victim.role
            })
        accomplice.accomplice_info = assign_accomplice_type(accomplice, murderer)
    for index, helper in enumerate(helpers):
        helper.set_relationships(
            {
                'role': _('Helper'),
                'knows_about': [victim.name],
                'victim_name': victim.name,
                'victim_role': victim.role
            })
        clue = murderer.murderer_info.clues['SecretClues'][index]
        helper.helper_info = assign_helper_type(helper, clue=clue)
    for neutral in neutral_npcs:
        neutral.set_relationships(
            {
                'role': _('Neutral'),
                'victim_name': victim.name,
                'victim_role': victim.role
            })

assign_relationships()

def get_person(role: str) -> Person or None:
    for npc in npc_list:
        if npc.role == role:
            return npc

    return None

def update_npc(npc, relationship_change):
    """Обновляет данные NPC после диалога."""
    npc.update_relationship(relationship_change)