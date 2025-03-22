import random
import gettext
import os
import json

# Localization setup
locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
gettext.bindtextdomain('messages', locale_dir)
gettext.textdomain('messages')
_ = gettext.gettext  # Translation function


def get_data(key: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), '../data/npc/npc.json'), 'r')
    loaded_data = json.load(file)
    result_list = []

    for item in loaded_data[key]:
        result_list.append(item)

    file.close()

    return result_list


class Person:
    def __init__(self, npc_id):
        self.id = npc_id
        self.role = get_data(key='roles')[npc_id]
        self.gender = 'Femail' if self.role in get_data('femail_roles') else 'Mail'
        self.personalities = []
        self.pressure_response = [random.choice(get_data(key='pressure_response'))]

        if self.gender == 'Femail':
            self.name = random.choice(get_data(key='femail_names'))
            self.personalities = ['lover']
            self.pressure_response.append('Flirt')
        else:
            self.name = random.choice(get_data(key='mail_names'))

        self.race = random.choice(get_data(key='races')) if self.role in get_data(key='non_humans') else 'Human'
        self.personalities.append(random.choice(get_data(key='personalities')))

        self.connections = {}  # Relationships between NPCs will be added later
        self.alibi = 'Unknown'
        self.knows_about = []
        self.suspect = False

    def __repr__(self):
        return f'<Person {self.name} ({self.role}), {self.race}, {self.personalities}, {self.pressure_response}>'

# Generate 10 NPCs
npc_list = [Person(i) for i in range(10)]

# Print NPC list
for npc in npc_list:
    print(npc)  # Later, this will be saved to a database
