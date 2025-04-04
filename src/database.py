from copy import deepcopy

from pymongo import MongoClient
import os

from src.npc_generator.npc_generator import get_npc_list
from src.accomplice_generator.accomlice_generator import Accomplice
from src.murderer_generator.murderer_generator import Ritualistic, Possessed, Avenger
from src.helper_generator.helper_generator import Helper

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "inquisition_game"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
saves_collection = db["saves"]

def save_game(save_slot="default"):
    """Сохраняет список NPC в MongoDB."""
    npc_list = deepcopy(get_npc_list())
    npc_data = [serialize_npc(npc) for npc in npc_list]

    save_data = {
        "slot": save_slot,
        "npc_list": npc_data
    }

    saves_collection.update_one(
        {"slot": save_slot},
        {"$set": save_data},
        upsert=True
    )

    print(f"✅ Игра сохранена в слот: {save_slot}")

def load_game(save_slot="default"):
    """Загружает сохранённое состояние игры из MongoDB."""
    save_data = saves_collection.find_one({"slot": save_slot})
    if save_data:
        print(f"✅ Игра загружена из слота: {save_slot}")
        return save_data  # Возвращаем словарь с NPC и другими данными
    print("⚠️ Сохранение не найдено!")
    return None

def serialize_npc(npc):
    """Сериализует NPC, включая вложенные объекты."""
    npc_data = npc.__dict__.copy()

    return npc_data

def get_save_slots():
    """Возвращает список всех доступных слотов сохранений."""
    return saves_collection.distinct("slot")

