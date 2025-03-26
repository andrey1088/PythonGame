from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "inquisition_game"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
saves_collection = db["saves"]

def save_game(game_state, save_slot="default"):
    """Сохраняет игру в MongoDB."""
    saves_collection.update_one(
        {"slot": save_slot},
        {"$set": game_state},
        upsert=True
    )
    print(f"✅ Игра сохранена в слот: {save_slot}")

def load_game(save_slot="default"):
    """Загружает сохранённое состояние игры."""
    save_data = saves_collection.find_one({"slot": save_slot})
    if save_data:
        print(f"✅ Игра загружена из слота: {save_slot}")
        return save_data
    print("⚠️ Сохранение не найдено!")
    return None
