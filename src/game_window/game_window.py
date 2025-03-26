import sys
import os
import importlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PyQt6.QtCore import Qt
from src.translation.translation import _

from src.abstract_npc.abstract_npc import AbstractNpc
from src.chat_system.chat_window import ChatWindow
from src.utils.window import create_menu_button, create_button
from src.game_window.game_dialog import NewGameDialog, LoadGameDialog, SaveGameDialog

from src.database import save_game, load_game

media_dir = os.path.join(os.path.dirname(__file__), "../media/")

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.get_npc = None
        self.chat_window = None
        self.centralWidget = None
        self.setWindowTitle("Inquisition Game")
        self.setGeometry(100, 100, 1024, 800)  # Устанавливаем квадратное окно
        self.setMinimumSize(1024, 800)  # Минимальный размер
        self.setMaximumSize(1024, 800)  # Максимальный размер
        self.is_game_started = False

        self.init_ui()

    def init_ui(self):
        self.create_start_page()

    def create_start_page(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{media_dir}places/main.png');")

        layout_wrapper = QHBoxLayout()
        layout_wrapper.setSpacing(0)

        menu_widget = self.create_main_menu()

        layout_wrapper.addWidget(menu_widget)
        central_widget.setLayout(layout_wrapper)
        central_widget.setContentsMargins(20, 20, 20, 20)

    def create_inquisitor_home(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{media_dir}places/inquisitor_home.png');")

        layout_wrapper = QHBoxLayout()
        layout_wrapper.setSpacing(0)

        right_column = self.create_right_column()
        left_column = self.create_left_column(title=_('To home'), button_link='to_start' )

        layout_wrapper.addWidget(left_column)
        layout_wrapper.addWidget(right_column)
        central_widget.setLayout(layout_wrapper)
        central_widget.setContentsMargins(20, 20, 20, 20)

    def create_map_page(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{media_dir}places/map.png');")

        layout_wrapper = QHBoxLayout()
        layout_wrapper.setSpacing(0)

        central_widget.setLayout(layout_wrapper)

        layout_inner = QGridLayout()
        layout_inner.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        left_column = self.create_left_column()

        stacked_widget = QWidget()
        stacked_widget.setLayout(layout_inner)
        stacked_widget.setStyleSheet("background: transparent;")
        stacked_widget.setMaximumWidth(340)
        layout_wrapper.addWidget(left_column)
        layout_wrapper.addWidget(stacked_widget)

        locations = {
            'tavern': self.show_tavern,
            'forge': self.show_blacksmith,
            'chapel': self.show_chapel,
            'market': self.show_market,
            'outskirts': self.show_forest,
            'abandoned_house': self.show_abandoned_house,
            'healers_place': self.show_healers_place,
            'hunters_place': self.show_hunters_place,
            'library': self.show_library,
            'torture': self.show_torture
        }

        row, col = 0, 0
        for name, action in locations.items():
            button = create_button(_(name), f'{media_dir}icons/{name}.png')
            button.setMaximumWidth(160)
            button.setMinimumWidth(160)
            button.clicked.connect(action)
            layout_inner.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def create_right_column(self):
        right_column = QWidget()
        layout = QVBoxLayout()
        right_column.setStyleSheet("background: transparent;")

        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        map_button = create_button(_('Map'), f'{media_dir}icons/map.png')
        map_button.setMaximumWidth(160)
        map_button.setMinimumWidth(160)
        map_button.clicked.connect(self.create_map_page)

        layout.addWidget(map_button)
        right_column.setLayout(layout)

        return right_column

    def create_left_column(self, title=_('Account'), button_link='to_account'):
        left_column = QWidget()
        layout = QVBoxLayout()
        left_column.setStyleSheet("background: transparent;")

        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        go_home_button = create_menu_button(title=title)
        save_game_button = create_menu_button(title=_('Save game'), is_disabled=not self.is_game_started)

        if button_link == 'to_start':
            go_home_button.clicked.connect(self.create_start_page)
        else:
            go_home_button.clicked.connect(self.create_inquisitor_home)

        save_game_button.clicked.connect(self.save_game)

        layout.addWidget(go_home_button)
        layout.addWidget(save_game_button)
        left_column.setLayout(layout)

        return left_column

    def create_main_menu(self):
        menu_widget = QWidget()
        menu_widget.setStyleSheet("""  
            background: transparent;
          """)

        layout_menu = QVBoxLayout()
        new_game_button = create_menu_button(_('New game'))
        continue_button = create_menu_button(_('Load game'))
        save_game_button = create_menu_button(title=_('Save game'), is_disabled=not self.is_game_started)
        exit_button = create_menu_button(_('Exit'))

        layout_menu.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        new_game_button.clicked.connect(self.start_new_game)
        continue_button.clicked.connect(self.load_game)
        save_game_button.clicked.connect(self.save_game)
        exit_button.clicked.connect(self.close)

        layout_menu.addWidget(new_game_button)
        layout_menu.addWidget(continue_button)
        layout_menu.addWidget(save_game_button)
        layout_menu.addWidget(exit_button)
        menu_widget.setLayout(layout_menu)

        return menu_widget

    def start_new_game(self):
        dlg = NewGameDialog(self)
        if dlg.exec():
            npc_generator = importlib.import_module("src.npc_generator.%s" % 'npc_generator')
            generate_npc = getattr(npc_generator, 'generate_npc')
            generate_npc()
            self.get_npc = getattr(npc_generator, 'get_npc')
            self.is_game_started = True
            self.create_inquisitor_home()
        else:
            print("Cancel!")

    def load_game(self):
        dlg = LoadGameDialog(self)
        if dlg.exec():
            game_data = load_game()
            if game_data:
                print("🎭 Продолжаем игру!")
                return game_data  # Используем загруженные данные
            else:
                print("⚠️ Сохранение не найдено. Начинаем заново.")
        else:
            print("Cancel!")

    def save_game(self):
        if self.is_game_started:
            dlg = SaveGameDialog(self)
            if dlg.exec():
                test_game_data = {'test date': 'some data'}
                save_game(test_game_data)
            else:
                print("Cancel!")

    def show_tavern(self):
        self.change_location(f'{media_dir}places/tavern.png', 'Innkeeper')

    def show_blacksmith(self):
        self.change_location(f'{media_dir}places/forge.png', 'Blacksmith')

    def show_chapel(self):
        self.change_location(f'{media_dir}places/chapel.png', 'Priest')

    def show_market(self):
        self.change_location(f'{media_dir}places/market.png', 'Merchant')

    def show_forest(self):
        self.change_location(f'{media_dir}places/outskirts.png', 'Wanderer')

    def show_abandoned_house(self):
        self.change_location(f'{media_dir}places/abandoned_house.png', 'Farmer')

    def show_healers_place(self):
        self.change_location(f'{media_dir}places/healers_place.png', 'Healer')

    def show_hunters_place(self):
        self.change_location(f'{media_dir}places/hunters_place.png', 'Hunter')

    def show_library(self):
        self.change_location(f'{media_dir}places/library.png')

    def show_torture(self):
        self.change_location(f'{media_dir}places/torture.png')

    def change_location(self, background, npc=None):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{background}');")

        layout_wrapper = QVBoxLayout()
        layout_wrapper.setSpacing(0)

        layout_inner = QHBoxLayout()
        widget_inner = QWidget()
        widget_inner.setLayout(layout_inner)
        widget_inner.setStyleSheet(f"background: transparent;")

        right_column = self.create_right_column()
        layout_inner.addWidget(right_column)

        layout_wrapper.addWidget(widget_inner)

        if npc is not None:
            person = self.get_npc(_(npc))
            avatar_button = create_button(person.name, f'{media_dir}avatars/{person.avatar}', 18)
            avatar_button.setMaximumWidth(200)
            layout_wrapper.addWidget(avatar_button)
            avatar_button.clicked.connect(lambda: self.start_chat(person))

        central_widget.setLayout(layout_wrapper)
        central_widget.setContentsMargins(20, 20, 20, 20)

    def start_chat(self, npc: AbstractNpc):
        self.chat_window = ChatWindow(npc)
        self.chat_window.exec()


def start_game():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())