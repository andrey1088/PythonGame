from npc_generator.npc_generator import npc_list
from src.abstract_npc.abstract_npc import AbstractNpc
from src.game_window.game_window import start_game

def chat_with_npc(npc: AbstractNpc):
    print(f"Вы разговариваете с {npc.name} ({npc.role})")

    while True:
        player_message = input("\nВы: ")

        if player_message.lower() in ["выход", "exit", "прощай"]:
            print(f"{npc.name}: Да пребудет с тобой удача, странник...")
            break

        npc_response = npc.get_response(player_message)
        print(f"\n{npc.name}: {npc_response}")

def main():
    start_game()
    pass

# chat_with_npc(npc_list[00])

if __name__ == "__main__":
    main()