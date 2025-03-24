from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import os

class ChatWindow(QDialog):
    def __init__(self, npc_name):
        super().__init__()

        self.setWindowTitle(f"Диалог с {npc_name}")
        self.setGeometry(300, 300, 500, 500)

        layout = QVBoxLayout()

        # Веб-вью для чата
        self.web_view = QWebEngineView()
        chat_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chat_ui.html"))
        self.web_view.setUrl(QUrl(f"file:///{chat_html_path}"))
        layout.addWidget(self.web_view)

        # Поле ввода и кнопка "Отправить"
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите сообщение...")
        self.send_button = QPushButton("Отправить")

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Подключаем отправку сообщений
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        player_text = self.input_field.text().strip()
        if player_text:
            js_code = f"addMessage('Вы', '{player_text}');"
            self.web_view.page().runJavaScript(js_code)
            self.input_field.clear()