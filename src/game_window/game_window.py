import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QScrollArea, QStackedWidget
from PyQt6.QtGui import QPixmap, QPicture, QImage
from PyQt6.QtCore import Qt
from src.translation.translation import _
from src.npc_generator.npc_generator import get_person
from src.abstract_npc.abstract_npc import AbstractNpc
from src.chat_system.chat_window import ChatWindow

from PyQt6 import uic

media_dir = os.path.join(os.path.dirname(__file__), "../media/")


def create_menu_button(title):
    map_button = QPushButton(title)
    map_button.setStyleSheet("""  
        QPushButton {
            background: rgba(0, 172, 252, 50);
            font-size: 14px;
            border: none;
            border-radius: 10px;
            padding: 20px;
            color: #fff;
        }
        QPushButton:hover {
            background: rgba(0, 172, 252, 50);
        }
      """)

    return map_button

def create_button(title, image_path, font_size=1):
    button = QPushButton(title)
    button.setStyleSheet(f"""  
        QPushButton {{
            background-image: url({image_path});
            background-repeat: no-repeat;
            background-position: center;
            font-size: {font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
            padding: 140px 10px 20px;
            color: #fff;
        }}
        QPushButton:hover {{
            opacity: 0.5;
        }}
      """)

    return button


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralWidget = None
        self.setWindowTitle("Inquisition Game")
        self.setGeometry(100, 100, 1024, 800)  # Устанавливаем квадратное окно
        self.setMinimumSize(1024, 800)  # Минимальный размер
        self.setMaximumSize(1024, 800)  # Максимальный размер

        self.init_ui()

    def init_ui(self):
        self.create_start_page()

    def create_start_page(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-image: url('{media_dir}places/main.png');")

        layout_wrapper = QHBoxLayout()
        layout_wrapper.setSpacing(0)

        right_column = self.create_right_column()
        menu_widget = self.create_main_menu()

        layout_wrapper.addWidget(menu_widget)
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

    def create_left_column(self):
        left_column = QWidget()
        layout = QVBoxLayout()
        left_column.setStyleSheet("background: transparent;")

        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        go_home_button = create_menu_button(title=_('Main page'))
        go_home_button.clicked.connect(self.create_start_page)

        layout.addWidget(go_home_button)
        left_column.setLayout(layout)

        return left_column

    def create_main_menu(self):
        menu_widget = QWidget()
        menu_widget.setStyleSheet("""  
            background: transparent;
          """)

        layout_menu = QVBoxLayout()
        menu_widget.setMaximumWidth(300)
        button_1 = create_menu_button(_('New game'))
        button_2 = create_menu_button('Продолжить')
        button_3 = create_menu_button('Выход')

        layout_menu.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        layout_menu.addWidget(button_1)
        layout_menu.addWidget(button_2)
        layout_menu.addWidget(button_3)
        menu_widget.setLayout(layout_menu)

        return menu_widget

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
        left_column = self.create_left_column()

        layout_inner.addWidget(left_column)
        layout_inner.addWidget(right_column)

        layout_wrapper.addWidget(widget_inner)

        if npc is not None:
            person = get_person(_(npc))
            avatar_button = create_button(person.name, f'{media_dir}avatars/{person.avatar}', 18)
            avatar_button.setMaximumWidth(200)
            layout_wrapper.addWidget(avatar_button)
            avatar_button.clicked.connect(self.start_chat(person))

        central_widget.setLayout(layout_wrapper)
        central_widget.setContentsMargins(20, 20, 20, 20)

    def start_chat(self, npc: AbstractNpc):
        self.chat_window = ChatWindow(npc.name)
        self.chat_window.exec()

    def chat_with_npc(npc: AbstractNpc):
        pass
    # print(f"Вы разговариваете с {npc.name} ({npc.role})")

    # while True:
    #     player_message = input("\nВы: ")
    #
    #     if player_message.lower() in ["выход", "exit", "прощай"]:
    #         print(f"{npc.name}: Да пребудет с тобой удача, странник...")
    #         break
    #
    #     npc_response = npc.get_response(player_message)
    #     print(f"\n{npc.name}: {npc_response}")


def start_game():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())