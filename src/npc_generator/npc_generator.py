import random
import gettext
import os
import json

# Localization setup
locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
gettext.bindtextdomain('messages', locale_dir)
gettext.textdomain('messages')
_ = gettext.gettext  # Translation function

def get_data(key: str) -> list:
    try:
        with open(os.path.join(os.path.dirname(__file__), '../data/npc/npc.json'), 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
            return loaded_data.get(key, [])
    except FileNotFoundError:
        print(_('Data file not found.'))
        return []
    except json.JSONDecodeError:
        print(_('Error decoding JSON data.'))
        return []

available_male_names = get_data('male_names')
available_female_names = get_data('female_names')

def assign_unique_name(available_names):
    name = random.choice(available_names)
    if len(available_names) > 1:
        available_names.remove(name)
    return name

class Person:
    used_names = set()  # To track assigned names

    def __init__(self, npc_id):
        self.id = npc_id
        self.role = get_data('roles')[npc_id]
        self.gender = 'Female' if self.role in get_data('female_roles') else 'Male'
        self.personalities = []
        self.pressure_response = [random.choice(get_data('pressure_response'))]
        if self.gender == 'Female':
            self.name = assign_unique_name(available_female_names)
            self.personalities = ['lover']
            self.pressure_response.append('flirt')
        else:
            self.name = assign_unique_name(available_male_names)
        self.race = random.choice(get_data('races')) if self.role in get_data('non_human_roles') else 'Human'
        self.personalities.append(random.choice(get_data(key='personalities')))

        self.alibi = 'Unknown'
        self.connections = {}
        self.knows_about = []
        self.suspect = False

    def __repr__(self):
        return f'<Person {self.name} ({self.role}), {self.gender}, {self.race}, {self.personalities}, {self.pressure_response}>'

# Generate NPCs
npc_list = [Person(i) for i in range(len(get_data('roles')))]

# Print NPC list
for npc in npc_list:
    print(npc)  # Later, this will be saved to a database
