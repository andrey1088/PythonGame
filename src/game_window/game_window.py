import sys
import os
import importlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QListWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from src.translation.translation import _

from src.abstract_npc.abstract_npc import AbstractNpc
from src.chat_system.chat_window import ChatWindow
from src.utils.window import create_menu_button, create_button
from src.game_window.game_dialog import NewGameDialog, LoadGameDialog, SaveGameDialog, AskForConfirmationDialog
from src.game_info.game_info import apply_loaded_data
from functools import partial

from src.database import save_game, load_game, get_save_slots

media_dir = os.path.join(os.path.dirname(__file__), "../media/")

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.get_npcs_by_location = None
        self.get_npc = None
        self.chat_window = None
        self.centralWidget = None
        self.ask_for_confirmation_dialog = None
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
            'tavern': lambda : self.change_location(background=f'{media_dir}places/tavern.png', location='tavern', inner_locations=None),
            'forge': lambda : self.change_location(background=f'{media_dir}places/forge.png', location='forge', inner_locations=None),
            'chapel': lambda : self.change_location(background=f'{media_dir}places/chapel.png', location='chapel', inner_locations=None),
            'market': lambda : self.change_location(background=f'{media_dir}places/market.png', location='market', inner_locations=None),
            'outskirts': lambda : self.change_location(background=f'{media_dir}places/outskirts.png', location='outskirts', inner_locations=None),
            'abandoned_house': lambda : self.change_location(background=f'{media_dir}places/abandoned_house.png', location='abandoned_house', inner_locations=None),
            'healers_place': lambda : self.change_location(background=f'{media_dir}places/healers_place.png', location='healers_place', inner_locations=None),
            'hunters_place': lambda : self.change_location(background=f'{media_dir}places/hunters_place.png', location='hunters_place', inner_locations=None),
            'library': lambda : self.change_location(background=f'{media_dir}places/library.png', location='library', inner_locations=None),
            'torture': lambda : self.change_location(background=f'{media_dir}places/torture.png', location='torture', inner_locations=None)
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

    def create_right_column(self, button=None):
        right_column = QWidget()
        layout = QVBoxLayout()
        right_column.setStyleSheet("background: transparent;")

        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        if not button:
            rendered_button = create_button(_('Map'), f'{media_dir}icons/map.png')
        else:
            rendered_button = create_button(_({button['']}), f'{media_dir}icons/map.png')

        rendered_button.setMaximumWidth(160)
        rendered_button.setMinimumWidth(160)
        rendered_button.clicked.connect(self.create_map_page)

        layout.addWidget(rendered_button)
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
        load_game_button = create_menu_button(_('Load game'))
        continue_button = create_menu_button(_('Continue'))
        save_game_button = create_menu_button(title=_('Save game'), is_disabled=not self.is_game_started)
        exit_button = create_menu_button(_('Exit'))

        layout_menu.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        new_game_button.clicked.connect(self.start_new_game)
        load_game_button.clicked.connect(self.load_game)
        save_game_button.clicked.connect(self.save_game)
        continue_button.clicked.connect(self.create_inquisitor_home)
        exit_button.clicked.connect(self.close)

        layout_menu.addWidget(new_game_button)
        layout_menu.addWidget(load_game_button)
        layout_menu.addWidget(save_game_button)

        if self.is_game_started:
            layout_menu.addWidget(continue_button)

        layout_menu.addWidget(exit_button)
        menu_widget.setLayout(layout_menu)

        return menu_widget

    def start_new_game(self):
        if self.is_game_started:
            self.ask_for_saving_game(self.create_new_game)
        else:
            self.create_new_game()

    def ask_for_saving_game(self, callback=None):
        self.ask_for_confirmation_dialog = AskForConfirmationDialog(
            self,
            title=_('Do you want to save game'),
            msg=_('There is no saved data. It will be lost. Do you want to save game?')
        )

        if self.ask_for_confirmation_dialog.exec():
            self.save_game(callback)
        elif callback:
            callback()


    def create_new_game(self):
        dlg = NewGameDialog(self)

        if dlg.exec():
            npc_generator = importlib.import_module("src.npc_generator.%s" % 'npc_generator')
            generate_npc = getattr(npc_generator, 'generate_npc')
            generate_npc()
            self.get_npc = getattr(npc_generator, 'get_npc')
            self.get_npcs_by_location = getattr(npc_generator, 'get_npcs_by_location')
            self.is_game_started = True
            self.create_inquisitor_home()
        else:
            print("Cancel!")

    def load_game(self):
        save_slots = get_save_slots()

        if not save_slots:
            print("⚠️ Нет сохранений!")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Выберите сохранение")

        layout = QVBoxLayout()
        list_widget = QListWidget()

        for slot in save_slots:
            list_widget.addItem(slot)

        layout.addWidget(list_widget)

        load_button = QPushButton("Загрузить")
        layout.addWidget(load_button)

        dialog.setLayout(layout)

        def on_load_clicked():
            selected_item = list_widget.currentItem()
            if selected_item:
                selected_slot = selected_item.text()
                game_data = load_game(selected_slot)
                if game_data:
                    apply_loaded_data(game_data)
                    dialog.accept()
                    npc_generator = importlib.import_module("src.npc_generator.%s" % 'npc_generator')
                    self.get_npc = getattr(npc_generator, 'get_npc')
                    self.get_npcs_by_location = getattr(npc_generator, 'get_npcs_by_location')
                    self.is_game_started = True
                    self.create_inquisitor_home()

        load_button.clicked.connect(on_load_clicked)

        dialog.exec()

    def save_game(self, callback=None):
        if self.is_game_started:
            dlg = SaveGameDialog(self)
            if dlg.exec():
                save_game(dlg.new_save_name)
                if callback:
                    callback()
            else:
                if self.ask_for_confirmation_dialog:
                    self.ask_for_confirmation_dialog.close()
                print("Cancel!")

    def show_torture(self):
        self.change_location(f'{media_dir}places/torture.png')

    def change_location(self, background, location='', inner_locations=None):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{background}');")

        layout_wrapper = QVBoxLayout()
        layout_wrapper.setSpacing(0)

        layout_inner = QHBoxLayout()
        layout_inner.setSpacing(0)
        layout_inner.setContentsMargins(0, 0, 0, 0)

        layout_bottom = QGridLayout()
        layout_bottom.setSpacing(0)
        layout_bottom.setContentsMargins(0, 0, 0, 0)

        widget_inner = QWidget()
        widget_bottom = QWidget()
        widget_inner.setLayout(layout_inner)
        widget_inner.setStyleSheet("background: transparent;")
        widget_bottom.setLayout(layout_bottom)
        widget_bottom.setStyleSheet("background: transparent;")

        right_column = self.create_right_column()
        layout_inner.addWidget(right_column)

        layout_wrapper.addWidget(widget_inner)

        npcs_by_location_list = self.get_npcs_by_location(location)

        if len(npcs_by_location_list):
            for index, npc in enumerate(npcs_by_location_list):
                if npc.connections['role'] != 'Victim':
                    avatar_button = create_button(npc.name, f'{media_dir}avatars/{npc.avatar}', 18)
                    avatar_button.setMaximumWidth(200)
                    avatar_button.setMinimumWidth(200)
                    avatar_button.setMaximumHeight(200)
                    avatar_button.clicked.connect(partial(self.start_chat, npc))
                    layout_bottom.addWidget(avatar_button, index, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        if inner_locations:
            for inner_location in inner_locations:
                inner_location_button = create_button(inner_location, f'{media_dir}icons/{inner_location}.png', 18)
                inner_location_button.setMaximumWidth(200)
                inner_location_button.setMinimumWidth(200)
                inner_location_button.setMaximumHeight(200)
                layout_bottom.addWidget(inner_location_button, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
                inner_location_button.clicked.connect(lambda: self.change_location(f'{media_dir}places/{inner_location}'))

        layout_wrapper.addWidget(widget_bottom)

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