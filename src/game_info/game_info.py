from src.npc_generator.npc_generator import generate_loaded_npc


class GameInfo:
    def __init__(self):
        self.current_page = 'start'

    def __repr__(self):
        return f"<Current page {self.current_page}>"

game_info = GameInfo()

def apply_loaded_data(data):
    print(data)
    loaded_npc_list = data['npc_list']
    generate_loaded_npc(loaded_npc_list)


