import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

npc_data = {
    'npc_id': 0,
    'avatar': '',
    'person_type': 'Citizen',
    'role': '',
    'gender':'',
    'personalities': None,
    'pressure_response': None,
    'murderer_info': None,
    'accomplice_info': None,
    'helper_info': None,
    'name': '',
    'race': '',
    'alibi': '',
    'connections': None,
    'suspect': False,
    'known_clues': None,
    'relationship_with_inquisitor': 0,
    'clues': None
}

class AbstractNpc:
    def __init__(self, npc_data, is_new=True):
        self.avatar = npc_data['avatar'] if 'avatar' in npc_data else ''
        self.person_type = npc_data['person_type'] if 'person_type' in npc_data else 'Citizen'
        self.npc_id = npc_data['npc_id'] if 'npc_id' in npc_data else 0
        self.role = npc_data['role'] if 'role' in npc_data else ''
        self.gender = npc_data['gender'] if 'gender' in npc_data else ''
        self.personalities = npc_data['personalities'] if 'personalities' in npc_data else []
        self.pressure_response = npc_data['pressure_response'] if 'pressure_response' in npc_data else []
        self.murderer_info = npc_data['murderer_info'] if 'murderer_info' in npc_data else []
        self.accomplice_info = npc_data['accomplice_info'] if 'accomplice_info' in npc_data else []
        self.helper_info = npc_data['helper_info'] if 'helper_info' in npc_data else []
        self.name = npc_data['name'] if 'name' in npc_data else ''
        self.race = npc_data['race'] if 'race' in npc_data else ''
        self.alibi = npc_data['alibi'] if 'alibi' in npc_data else ''
        self.connections = npc_data['connections']if 'person_type' in npc_data else {}
        self.suspect = npc_data['suspect'] if 'suspect' in npc_data else False
        self.known_clues = npc_data['known_clues'] if 'known_clues' in npc_data else []
        self.relationship_with_inquisitor = npc_data['relationship_with_inquisitor'] if 'relationship_with_inquisitor' in npc_data else 0
        self.clues = npc_data['clues'] if 'clues' in npc_data else []

    def get_response(self, player_message):
        """Генерация ответа NPC через ChatGPT"""
        prompt = f"""Ты – {self.name}, {self.role} в средневековой деревне. 
        Твой характер – {self.personalities}.  
        Ответь в стиле средневекового фэнтези, соответствуя своему характеру."""

        client = OpenAI()

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=prompt,
            input=f'{player_message}'
        )

        return response.output_text

    def set_relationships(self, relationships: dict) -> None:
        self.connections = relationships

    def update_relationship(self, change):
        """Изменяет отношение NPC к инквизитору."""
        self.relationship_with_inquisitor += change