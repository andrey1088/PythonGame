import random
import json
import os
from translation import _

def generate_npc(npc_id):
    names = get_data(key='names')
    roles = get_data(key='roles')
    races = get_data(key='races')
    non_humans = get_data(key='non_humans')
    personalities = get_data(key='personalities')

    npc = {
        "id": npc_id,
        "name": random.choice(names),
        "role": roles[npc_id],  # Each NPC is assigned a unique role
        "race": random.choice(races) if roles[npc_id] in non_humans else _("Human"),
        "personality": random.choice(personalities),
        "pressure_response": random.choice(["Persuasion", "Threats", "Bribery", "Blackmail", "Flirt"]),
        "connections": {},  # Relationships between NPCs will be added later
        "alibi": "Unknown",
        "knows_about": [],
        "suspect": False
    }

    return npc

def get_data(*, key: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), "../data/npc/npc.json"), 'r')
    loaded_data = json.load(file)
    result_list = []

    for item in loaded_data[key]:
        result_list.append(item)

    file.close()

    return result_list

def print_npc_list():
    names = get_data(key='names')

    npc_list = [generate_npc(i) for i in range(len(names))]

    # Print NPC list
    for npc in npc_list:
        print(npc)  # Later, this will be saved to a database

if __name__ == "__main__":
    print_npc_list()