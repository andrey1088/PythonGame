class GameInfo:
    def __init__(self):
        self.current_page = 'start'

    def __repr__(self):
        return f"<Current page {self.current_page}>"

game_info = GameInfo()

