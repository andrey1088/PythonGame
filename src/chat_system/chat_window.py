import openai
from openai import OpenAI
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

from src.abstract_npc.abstract_npc import AbstractNpc
from src.npc_generator.npc_generator import update_npc
from src.inquisitor.inquisitor import inquisitor

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def calculate_relationship_change(value: bool):
    """Пример расчёта изменения отношений NPC после диалога."""
    return 1 if value else -1  # Здесь можно добавить сложную логику


class ChatWindow(QDialog):
    def __init__(self, npc: AbstractNpc):
        super().__init__()

        self.npc = npc

        self.npc_name = npc.name
        self.setWindowTitle(f"Диалог с {npc.name}")
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

        self.close_button = QPushButton("Закончить диалог")
        self.close_button.clicked.connect(self.end_chat)
        layout.addWidget(self.close_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        player_text = self.input_field.text().strip()
        if player_text:
            # Добавляем сообщение игрока в чат
            js_code = f"addMessage('Вы', '{player_text}');"
            self.web_view.page().runJavaScript(js_code)

            # Отправляем запрос в ChatGPT
            response = self.get_npc_response(player_text)
            if response:
                npc_response = response.strip()
                js_code = f"addMessage('{self.npc_name}', '{npc_response}');"
                self.web_view.page().runJavaScript(js_code)

            self.input_field.clear()

    def get_npc_response(self, player_text):
        """Запрос к ChatGPT для генерации ответа NPC."""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI()

        """Генерация ответа NPC через ChatGPT"""
        prompt = f"""Ты – {self.npc.name}, {self.npc.role} в средневековой деревне. 
                Твой характер – {self.npc.personalities}.  
                В твоей деревне произошло убийство. 
                Жертва - {self.npc.connections['victim_role']} по имени {self.npc.connections['victim_name']}
                Ты разговариваешь с инквизитором, который прибыл для расследования.
                Ответь в стиле средневекового фэнтези, соответствуя своему характеру."""

        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                instructions=prompt,
                input=f'{player_text}'
            )

            return response.output_text
        except Exception as e:
            print("Ошибка API:", e)
            return "Я не знаю, что сказать..."

    def end_chat(self):
        """Закрытие чата с обновлением данных NPC."""
        relationship_change = calculate_relationship_change(True)
        update_npc(self.npc, relationship_change)
        self.close()

    def closeEvent(self, event):
        """Вызывается при закрытии окна чата (например, крестиком)."""
        self.end_chat()
        event.accept()