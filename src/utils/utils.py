from src.translation.translation import _
import os
import json

def get_data(key: str, path: str) -> list:
    try:
        with open(os.path.join(os.path.dirname(__file__), f'../data/{path}.json'), 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
            return loaded_data.get(key, [])
    except FileNotFoundError:
        print(_('Data file not found.'))
        return []
    except json.JSONDecodeError:
        print(_('Error decoding JSON data.'))
        return []