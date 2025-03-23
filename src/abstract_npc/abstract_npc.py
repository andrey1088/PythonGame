import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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