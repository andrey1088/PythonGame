import random
from src.translation.translation import _
from src.murderer_generator.murderer_generator import assign_murderer_type
from src.utils.utils import get_data

available_male_names = get_data('male_names')
available_female_names = get_data('female_names')

def assign_unique_name(available_names):
    name = random.choice(available_names)
    if len(available_names) > 1:
        available_names.remove(name)
    return _(name)

class Person:
    used_names = set()  # To track assigned names

    def __init__(self, npc_id):
        self.id = npc_id
        self.role = _(get_data('roles')[npc_id])
        self.gender = _('Female') if get_data('roles')[npc_id] in get_data('female_roles') else _('Male')
        self.personalities = []
        self.pressure_response = [_(random.choice(get_data('pressure_response')))]
        self.murderer_type = None
        if self.gender == _('Female'):
            self.name = assign_unique_name(available_female_names)
            self.personalities = []
            self.personalities.append(_('Lover'))
            self.pressure_response.append(_('flirt'))
        else:
            self.name = assign_unique_name(available_male_names)
        race = random.choice(get_data('races'))
        self.race = _(race) if self.role in get_data(key='non_humans') else _('Human')
        self.personalities.append(_(random.choice(get_data(key='personalities'))))

        self.alibi = 'Unknown'
        self.connections = {}
        self.knows_about = []
        self.suspect = False

    def set_relationships(self, relationships: dict) -> None:
        self.connections = relationships

    def __repr__(self):
        return str({
            'name': self.name,
            'role': self.role,
            'personalities': self.personalities,
            'pressure_response': self.pressure_response,
            'connections': self.connections,
            'murderer_info': self.murderer_type
        })

# Generate NPCs
npc_list = [Person(i) for i in range(len(get_data('roles')))]

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
            murderer.murderer_type = assign_murderer_type(murderer)
        else:
            victim = main_npcs[i]

    # Assign 2 accomplices, 3 helpers, and 2 neutrals
    accomplices = random.sample([npc for npc in npc_list if npc not in main_npcs], 2)
    helpers = random.sample([npc for npc in npc_list if npc not in accomplices and npc not in main_npcs], 3)
    neutral_npcs = [npc for npc in npc_list if npc not in accomplices and npc not in helpers and npc not in main_npcs]

    # Set connections
    for accomplice in accomplices:
        accomplice.set_relationships({'role': _('Accomplice'), 'knows_about': [murderer.name]})
    for helper in helpers:
        helper.set_relationships({'role': _('Helper'), 'knows_about': [victim.name]})
    for neutral in neutral_npcs:
        neutral.set_relationships({'role': _('Neutral')})

assign_relationships()

for item in npc_list:
    print(item)