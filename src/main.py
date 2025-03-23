from npc_generator.npc_generator import npc_list
from src.abstract_npc.abstract_npc import AbstractNpc

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = None
        self.layout = None
        self.central_widget = None
        self.current_background = 'media/places/main.png'
        self.map_button = None
        self.setWindowTitle("Inquisition Game")

        self.setGeometry(100, 100, 800, 800)  # Устанавливаем квадратное окно
        self.setMinimumSize(600, 600)  # Минимальный размер
        self.setMaximumSize(1200, 1200)  # Максимальный размер

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Создаем область прокрутки для фонового изображения (только по Y)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area.setWidget(self.label)
        self.layout.addWidget(self.scroll_area)

        self.map_button = QPushButton("Карта", self)
        self.map_button.clicked.connect(self.show_map)
        self.layout.addWidget(self.map_button)

        self.central_widget.setLayout(self.layout)

        self.show_background("media/places/main.png")

    def show_background(self, image_path):
        self.current_background = image_path
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Обновляет фон при изменении размера окна."""
        self.show_background(self.current_background)
        super().resizeEvent(event)

    def clear_layout(self):
        while self.layout.count() > 1:  # Оставляем только фон
            item = self.layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()

    def show_map(self):
        self.current_background = "media/places/map.png"
        self.show_background(self.current_background)

        self.clear_layout()

        # Создание сетки для кнопок локаций
        grid_layout = QGridLayout()

        locations = {
            "Таверна": self.show_tavern,
            "Кузница": self.show_blacksmith,
            "Часовня": self.show_chapel,
            "Рынок": self.show_market,
            "Лес": self.show_forest
        }

        row, col = 0, 0
        for name, action in locations.items():
            button = QPushButton(name)
            button.clicked.connect(action)
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.layout.addWidget(self.label)
        self.layout.addLayout(grid_layout)
        self.map_button = QPushButton("На главную")
        self.map_button.clicked.connect(self.show_main)
        self.layout.addWidget(self.map_button)

    def show_main(self):
        self.current_background = "media/places/main.png"
        self.show_background(self.current_background)

        self.clear_layout()

        self.layout.addWidget(self.label)
        self.map_button = QPushButton("Карта")
        self.map_button.clicked.connect(self.show_map)
        self.layout.addWidget(self.map_button)

    def show_tavern(self):
        self.change_location("media/places/tavern.png")

    def show_blacksmith(self):
        self.change_location("media/places/forge.png")

    def show_chapel(self):
        self.change_location("media/places/chapel.png")

    def show_market(self):
        self.change_location("media/places/market.png")

    def show_forest(self):
        self.change_location("media/places/outskirts.png")

    def change_location(self, background):
        self.current_background = background
        self.show_background(background)

        self.clear_layout()

        self.layout.addWidget(self.label)
        self.map_button = QPushButton("Карта")
        self.map_button.clicked.connect(self.show_map)
        self.layout.addWidget(self.map_button)


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
    # Основная логика игры
    pass

# chat_with_npc(npc_list[00])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())