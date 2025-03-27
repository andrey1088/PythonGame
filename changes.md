diff --git a/src/abstract_npc/abstract_npc.py b/src/abstract_npc/abstract_npc.py
index 7a0fb70..0528364 100644
--- a/src/abstract_npc/abstract_npc.py
+++ b/src/abstract_npc/abstract_npc.py
@@ -6,24 +6,47 @@ load_dotenv()
 
 OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
 
+npc_data = {
+    'npc_id': 0,
+    'avatar': '',
+    'person_type': 'Citizen',
+    'role': '',
+    'gender':'',
+    'personalities': None,
+    'pressure_response': None,
+    'murderer_info': None,
+    'accomplice_info': None,
+    'helper_info': None,
+    'name': '',
+    'race': '',
+    'alibi': '',
+    'connections': None,
+    'suspect': False,
+    'known_clues': None,
+    'relationship_with_inquisitor': 0,
+    'clues': None
+}
+
 class AbstractNpc:
-    def __init__(self):
-        self.id = ''
-        self.role = ''
-        self.gender = ''
-        self.personalities = []
-        self.pressure_response = []
-        self.murderer_info = None
-        self.accomplice_info = None
-        self.helper_info = None
-        self.name = ''
-        self.personalities = []
-        self.race = ''
-        self.alibi = ''
-        self.connections = {}
-        self.suspect = False
-        self.known_clues = []
-        self.relationship_with_inquisitor = 0
+    def __init__(self, npc_data, is_new=True):
+        self.avatar = npc_data['avatar'] if 'avatar' in npc_data else ''
+        self.person_type = npc_data['person_type'] if 'person_type' in npc_data else 'Citizen'
+        self.npc_id = npc_data['npc_id'] if 'npc_id' in npc_data else 0
+        self.role = npc_data['role'] if 'role' in npc_data else ''
+        self.gender = npc_data['gender'] if 'gender' in npc_data else ''
+        self.personalities = npc_data['personalities'] if 'personalities' in npc_data else []
+        self.pressure_response = npc_data['pressure_response'] if 'pressure_response' in npc_data else []
+        self.murderer_info = npc_data['murderer_info'] if 'murderer_info' in npc_data else []
+        self.accomplice_info = npc_data['accomplice_info'] if 'accomplice_info' in npc_data else []
+        self.helper_info = npc_data['helper_info'] if 'helper_info' in npc_data else []
+        self.name = npc_data['name'] if 'name' in npc_data else ''
+        self.race = npc_data['race'] if 'race' in npc_data else ''
+        self.alibi = npc_data['alibi'] if 'alibi' in npc_data else ''
+        self.connections = npc_data['connections']if 'person_type' in npc_data else {}
+        self.suspect = npc_data['suspect'] if 'suspect' in npc_data else False
+        self.known_clues = npc_data['known_clues'] if 'known_clues' in npc_data else []
+        self.relationship_with_inquisitor = npc_data['relationship_with_inquisitor'] if 'relationship_with_inquisitor' in npc_data else 0
+        self.clues = npc_data['clues'] if 'clues' in npc_data else []
 
     def get_response(self, player_message):
         """Генерация ответа NPC через ChatGPT"""
@@ -39,4 +62,11 @@ class AbstractNpc:
             input=f'{player_message}'
         )
 
-        return response.output_text
\ No newline at end of file
+        return response.output_text
+
+    def set_relationships(self, relationships: dict) -> None:
+        self.connections = relationships
+
+    def update_relationship(self, change):
+        """Изменяет отношение NPC к инквизитору."""
+        self.relationship_with_inquisitor += change
\ No newline at end of file
diff --git a/src/accomplice_generator/accomlice_generator.py b/src/accomplice_generator/accomlice_generator.py
index d74792c..36e7f3d 100644
--- a/src/accomplice_generator/accomlice_generator.py
+++ b/src/accomplice_generator/accomlice_generator.py
@@ -1,25 +1,25 @@
 from src.abstract_npc.abstract_npc import AbstractNpc
 
-class Accomplice:
-    def __init__(self, npc):
-        super().__init__()
-        self.name = 'Accomplice'
+class Accomplice(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type = 'Accomplice'
         self.clues = []
-        self.killer = []
+        self.murderer = []
 
     def assign_clues(self, clues):
         """Сообщник знает все улики убийцы."""
-        self.clues = clues
+        self.clues = clues['SecretClues']
 
-    def assign_killer_info(self, killer):
+    def assign_murderer_info(self, murderer):
         """Сообщник знает все улики убийцы."""
-        self.killer = killer
+        self.murderer = murderer
 
 # Function to randomly assign a murderer type
-def assign_accomplice_type(npc: AbstractNpc, killer: AbstractNpc) -> Accomplice:
+def assign_accomplice_type(npc, murderer) -> Accomplice:
     accomplice = Accomplice(npc)
-    accomplice.assign_clues(killer.murderer_info.clues)
-    accomplice.assign_killer_info(killer)
+    accomplice.assign_clues(murderer['clues'])
+    accomplice.assign_murderer_info(murderer)
 
     return accomplice
 
diff --git a/src/data/clues.json b/src/data/clues.json
index 0e928fd..41432d9 100644
--- a/src/data/clues.json
+++ b/src/data/clues.json
@@ -1,5 +1,5 @@
 {
-    "Ritualist": {
+    "Ritualistic": {
         "PublicClues": [
             "Жертва была найдена в необычном месте.",
             "Несколько жителей слышали крики поздно ночью.",
@@ -36,7 +36,7 @@
             "Пропавшее оружие из дома убийцы совпадает с раной жертвы."
         ]
     },
-    "AccidentalKiller": {
+    "Accidental": {
         "PublicClues": [
             "Жертва была замечена в таверне в ночь убийства.",
             "Очевидцы говорят, что жертва выглядела очень взволнованной перед смертью.",
diff --git a/src/database.py b/src/database.py
index 938d98b..c2665e2 100644
--- a/src/database.py
+++ b/src/database.py
@@ -5,7 +5,7 @@ import os
 
 from src.npc_generator.npc_generator import get_npc_list
 from src.accomplice_generator.accomlice_generator import Accomplice
-from src.murderer_generator.murderer_generator import Ritualist, Possessed, Avenger
+from src.murderer_generator.murderer_generator import Ritualistic, Possessed, Avenger
 from src.helper_generator.helper_generator import Helper
 
 MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
@@ -34,11 +34,11 @@ def save_game(save_slot="default"):
     print(f"✅ Игра сохранена в слот: {save_slot}")
 
 def load_game(save_slot="default"):
-    """Загружает сохранённое состояние игры."""
+    """Загружает сохранённое состояние игры из MongoDB."""
     save_data = saves_collection.find_one({"slot": save_slot})
     if save_data:
         print(f"✅ Игра загружена из слота: {save_slot}")
-        return save_data
+        return save_data  # Возвращаем словарь с NPC и другими данными
     print("⚠️ Сохранение не найдено!")
     return None
 
@@ -47,15 +47,20 @@ def serialize_npc(npc):
     npc_data = npc.__dict__.copy()
 
     # Преобразуем вложенные объекты, если они есть
-    if isinstance(npc_data.get('accomplice_info'), Accomplice):
-        npc_data['accomplice_info'] = npc_data['accomplice_info'].__dict__
-        npc_data['accomplice_info']['killer'] = npc_data['accomplice_info']['killer'].__dict__
-        if not type(npc_data['accomplice_info']['killer']['murderer_info']) is dict:
-            npc_data['accomplice_info']['killer']['murderer_info'] = npc_data['accomplice_info']['killer']['murderer_info'].__dict__
-    if isinstance(npc_data.get('helper_info'), Helper):
-        npc_data['helper_info'] = npc_data['helper_info'].__dict__
-
-    if isinstance(npc_data.get('murderer_info'), Ritualist) or isinstance(npc_data.get('murderer_info'), Possessed) or isinstance(npc_data.get('murderer_info'), Avenger):
-        npc_data['murderer_info'] = npc_data['murderer_info'].__dict__
+    # if isinstance(npc_data.get('accomplice_info'), Accomplice):
+    #     npc_data['accomplice_info'] = npc_data['accomplice_info'].__dict__
+    #     npc_data['accomplice_info']['killer'] = npc_data['accomplice_info']['killer'].__dict__
+    #     if not type(npc_data['accomplice_info']['killer']['murderer_info']) is dict:
+    #         npc_data['accomplice_info']['killer']['murderer_info'] = npc_data['accomplice_info']['killer']['murderer_info'].__dict__
+    # if isinstance(npc_data.get('helper_info'), Helper):
+    #     npc_data['helper_info'] = npc_data['helper_info'].__dict__
+    #
+    # if isinstance(npc_data.get('murderer_info'), Ritualist) or isinstance(npc_data.get('murderer_info'), Possessed) or isinstance(npc_data.get('murderer_info'), Avenger):
+    #     npc_data['murderer_info'] = npc_data['murderer_info'].__dict__
 
     return npc_data
+
+def get_save_slots():
+    """Возвращает список всех доступных слотов сохранений."""
+    return saves_collection.distinct("slot")
+
diff --git a/src/game_info/game_info.py b/src/game_info/game_info.py
index d25991b..1496a05 100644
--- a/src/game_info/game_info.py
+++ b/src/game_info/game_info.py
@@ -1,3 +1,6 @@
+from src.npc_generator.npc_generator import generate_loaded_npc
+
+
 class GameInfo:
     def __init__(self):
         self.current_page = 'start'
@@ -7,3 +10,9 @@ class GameInfo:
 
 game_info = GameInfo()
 
+def apply_loaded_data(data):
+    print(data)
+    loaded_npc_list = data['npc_list']
+    generate_loaded_npc(loaded_npc_list)
+
+
diff --git a/src/game_window/game_window.py b/src/game_window/game_window.py
index 8128467..b769474 100644
--- a/src/game_window/game_window.py
+++ b/src/game_window/game_window.py
@@ -1,7 +1,7 @@
 import sys
 import os
 import importlib
-from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
+from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QListWidget, QPushButton
 from PyQt6.QtCore import Qt
 from src.translation.translation import _
 
@@ -9,8 +9,9 @@ from src.abstract_npc.abstract_npc import AbstractNpc
 from src.chat_system.chat_window import ChatWindow
 from src.utils.window import create_menu_button, create_button
 from src.game_window.game_dialog import NewGameDialog, LoadGameDialog, SaveGameDialog
+from src.game_info.game_info import apply_loaded_data
 
-from src.database import save_game, load_game
+from src.database import save_game, load_game, get_save_slots
 
 media_dir = os.path.join(os.path.dirname(__file__), "../media/")
 
@@ -157,20 +158,26 @@ class GameWindow(QMainWindow):
 
         layout_menu = QVBoxLayout()
         new_game_button = create_menu_button(_('New game'))
-        continue_button = create_menu_button(_('Load game'))
+        load_game_button = create_menu_button(_('Load game'))
+        continue_button = create_menu_button(_('Continue'))
         save_game_button = create_menu_button(title=_('Save game'), is_disabled=not self.is_game_started)
         exit_button = create_menu_button(_('Exit'))
 
         layout_menu.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
 
         new_game_button.clicked.connect(self.start_new_game)
-        continue_button.clicked.connect(self.load_game)
+        load_game_button.clicked.connect(self.load_game)
         save_game_button.clicked.connect(self.save_game)
+        continue_button.clicked.connect(self.create_inquisitor_home)
         exit_button.clicked.connect(self.close)
 
         layout_menu.addWidget(new_game_button)
-        layout_menu.addWidget(continue_button)
+        layout_menu.addWidget(load_game_button)
         layout_menu.addWidget(save_game_button)
+
+        if self.is_game_started:
+            layout_menu.addWidget(continue_button)
+
         layout_menu.addWidget(exit_button)
         menu_widget.setLayout(layout_menu)
 
@@ -189,16 +196,46 @@ class GameWindow(QMainWindow):
             print("Cancel!")
 
     def load_game(self):
-        dlg = LoadGameDialog(self)
-        if dlg.exec():
-            game_data = load_game()
-            if game_data:
-                print("🎭 Продолжаем игру!")
-                return game_data  # Используем загруженные данные
-            else:
-                print("⚠️ Сохранение не найдено. Начинаем заново.")
-        else:
-            print("Cancel!")
+        """Вызывается при нажатии кнопки 'Загрузить игру'."""
+        save_slots = get_save_slots()
+
+        if not save_slots:
+            print("⚠️ Нет сохранений!")
+            return
+
+        dialog = QDialog(self)
+        dialog.setWindowTitle("Выберите сохранение")
+
+        layout = QVBoxLayout()
+        list_widget = QListWidget()
+
+        # Добавляем слоты в список
+        for slot in save_slots:
+            list_widget.addItem(slot)
+
+        layout.addWidget(list_widget)
+
+        load_button = QPushButton("Загрузить")
+        layout.addWidget(load_button)
+
+        dialog.setLayout(layout)
+
+        def on_load_clicked():
+            selected_item = list_widget.currentItem()
+            if selected_item:
+                selected_slot = selected_item.text()
+                game_data = load_game(selected_slot)
+                if game_data:
+                    apply_loaded_data(game_data)
+                    dialog.accept()
+                    npc_generator = importlib.import_module("src.npc_generator.%s" % 'npc_generator')
+                    self.get_npc = getattr(npc_generator, 'get_npc')
+                    self.is_game_started = True
+                    self.create_inquisitor_home()
+
+        load_button.clicked.connect(on_load_clicked)
+
+        dialog.exec()
 
     def save_game(self):
         if self.is_game_started:
@@ -258,10 +295,11 @@ class GameWindow(QMainWindow):
 
         if npc is not None:
             person = self.get_npc(_(npc))
-            avatar_button = create_button(person.name, f'{media_dir}avatars/{person.avatar}', 18)
-            avatar_button.setMaximumWidth(200)
-            layout_wrapper.addWidget(avatar_button)
-            avatar_button.clicked.connect(lambda: self.start_chat(person))
+            if person.connections['role'] != 'Victim':
+                avatar_button = create_button(person.name, f'{media_dir}avatars/{person.avatar}', 18)
+                avatar_button.setMaximumWidth(200)
+                layout_wrapper.addWidget(avatar_button)
+                avatar_button.clicked.connect(lambda: self.start_chat(person))
 
         central_widget.setLayout(layout_wrapper)
         central_widget.setContentsMargins(20, 20, 20, 20)
diff --git a/src/helper_generator/helper_generator.py b/src/helper_generator/helper_generator.py
index e2630f8..10c134c 100644
--- a/src/helper_generator/helper_generator.py
+++ b/src/helper_generator/helper_generator.py
@@ -1,9 +1,9 @@
 from src.abstract_npc.abstract_npc import AbstractNpc
 
-class Helper:
-    def __init__(self, npc):
-        super().__init__()
-        self.name = 'Helper'
+class Helper(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type = 'Helper'
         self.clues = []
 
     def assign_clues(self, clue):
@@ -11,7 +11,7 @@ class Helper:
         self.clues.append(clue)
 
 # Function to randomly assign a murderer type
-def assign_helper_type(npc: AbstractNpc, clue: str) -> Helper:
+def assign_helper_type(npc, clue: str) -> Helper:
     helper = Helper(npc)
     helper.assign_clues(clue)
 
diff --git a/src/murderer_generator/murderer_generator.py b/src/murderer_generator/murderer_generator.py
index bd46e1f..5cf055a 100644
--- a/src/murderer_generator/murderer_generator.py
+++ b/src/murderer_generator/murderer_generator.py
@@ -1,35 +1,28 @@
 import random
-from abc import ABC, abstractmethod
-from pyclbr import Class
-from src.abstract_npc.abstract_npc import AbstractNpc
 from src.utils.utils import get_data
+from src.abstract_npc.abstract_npc import AbstractNpc
 
-class MurdererType(ABC):
-    def __init__(self, killer: AbstractNpc):
-        self.killer = killer  # Убийца, связанный с этим типом
-        self.clues = self.generate_clue() # Улики, связанные с убийством
-        self.method = self.murder_method() # Метод убийства
-
-    @abstractmethod
-    def generate_clue(self):
-        """Генерирует уникальную улику для данного типа убийцы."""
-        pass
-
-    @abstractmethod
-    def murder_method(self):
-        """Возвращает способ убийства."""
-        pass
-
+class Ritualistic(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type = 'Ritualistic'
+        self.clues = self.generate_clue()  # Улики, связанные с убийством
+        self.method = self.murder_method()  # Метод убийства
 
-class Ritualist(MurdererType):
     def generate_clue(self):
-        return get_data('Ritualist', 'clues')
+        return get_data('Ritualistic', 'clues')
 
     def murder_method(self):
         return "The victim was sacrificed in a dark ritual."
 
 
-class Possessed(MurdererType):
+class Possessed(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type = 'Possessed'
+        self.clues = self.generate_clue()
+        self.method = self.murder_method()
+
     def generate_clue(self):
         return get_data('Possessed', 'clues')
 
@@ -37,7 +30,13 @@ class Possessed(MurdererType):
         return "The murderer was possessed and had no control over their actions."
 
 
-class Avenger(MurdererType):
+class Avenger(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type='Avenger'
+        self.clues = self.generate_clue()  # Улики, связанные с убийством
+        self.method = self.murder_method()  # Метод убийства
+
     def generate_clue(self):
         return get_data('Avenger', 'clues')
 
@@ -45,17 +44,24 @@ class Avenger(MurdererType):
         return "The murderer acted out of revenge."
 
 
-class AccidentalKiller(MurdererType):
+class Accidental(AbstractNpc):
+    def __init__(self, npc, is_new=True):
+        super().__init__(npc, is_new)
+        self.person_type='Accidental'
+        self.clues = self.generate_clue()  # Улики, связанные с убийством
+        self.method = self.murder_method()  # Метод убийства
+
     def generate_clue(self):
-        return get_data('AccidentalKiller', 'clues')
+        return get_data('Accidental', 'clues')
 
     def murder_method(self):
         return "The murder happened unintentionally during a conflict."
 
 
 # Function to randomly assign a murderer type
-def assign_murderer_type(npc: AbstractNpc) -> Class:
-    murderer_classes = [Ritualist, Possessed, Avenger, AccidentalKiller]
-    return random.choice(murderer_classes)(npc.name)
+def assign_murderer_type(npc) -> AbstractNpc:
+    murderer_classes = [Ritualistic, Possessed, Avenger, Accidental]
+    murderer = random.choice(murderer_classes)(npc)
+    return murderer
 
 
diff --git a/src/npc_generator/npc_generator.py b/src/npc_generator/npc_generator.py
index 5a7441d..3dc36dd 100644
--- a/src/npc_generator/npc_generator.py
+++ b/src/npc_generator/npc_generator.py
@@ -1,10 +1,10 @@
 import random
 from src.translation.translation import _
-from src.murderer_generator.murderer_generator import assign_murderer_type
-from src.accomplice_generator.accomlice_generator import assign_accomplice_type
-from src.helper_generator.helper_generator import assign_helper_type
+from src.murderer_generator.murderer_generator import assign_murderer_type, Ritualistic, Possessed, Avenger, Accidental
+from src.accomplice_generator.accomlice_generator import assign_accomplice_type, Accomplice
+from src.helper_generator.helper_generator import assign_helper_type, Helper
 from src.utils.utils import get_data
-from src.abstract_npc.abstract_npc import AbstractNpc
+from src.abstract_npc.abstract_npc import AbstractNpc, npc_data
 
 available_male_names = get_data('male_names', 'npc')
 available_female_names = get_data('female_names', 'npc')
@@ -18,14 +18,12 @@ def assign_unique_name(available_names):
 class Person(AbstractNpc):
     used_names = set()  # To track assigned names
 
-    def __init__(self, npc_id, is_new=True):
-        super().__init__()
-        self.id = npc_id
-
+    def __init__(self, data, is_new=True):
+        super().__init__(npc_data=data, is_new=True)
         if is_new:
-            self.role = _(get_data('roles', 'npc')[npc_id])
-            self.avatar = f"{get_data('roles', 'npc')[npc_id]}.png"
-            self.gender = _('Female') if get_data('roles', 'npc')[npc_id] in get_data('female_roles', 'npc') else _(
+            self.role = _(get_data('roles', 'npc')[data['npc_id']])
+            self.avatar = f"{get_data('roles', 'npc')[data['npc_id']]}.png"
+            self.gender = _('Female') if get_data('roles', 'npc')[data['npc_id']] in get_data('female_roles', 'npc') else _(
                 'Male')
             self.personalities = []
             self.pressure_response = [_(random.choice(get_data('pressure_response', 'npc')))]
@@ -39,7 +37,7 @@ class Person(AbstractNpc):
             else:
                 self.name = assign_unique_name(available_male_names)
             race = _('Vampire') if self.role == _('Wanderer') else random.choice(get_data('races', 'npc'))
-            self.race = _(race) if get_data('roles', 'npc')[npc_id] in get_data('non_humans', 'npc') else _('Human')
+            self.race = _(race) if get_data('roles', 'npc')[data['npc_id']] in get_data('non_humans', 'npc') else _('Human')
             self.personalities.append(_(random.choice(get_data('personalities', 'npc'))))
 
             self.alibi = 'Unknown'
@@ -47,9 +45,6 @@ class Person(AbstractNpc):
             self.suspect = False
             self.known_clues = []
 
-    def set_relationships(self, relationships: dict) -> None:
-        self.connections = relationships
-
     def get_clues(self, pressure_method):
         """Определяет, какие улики NPC готов раскрыть в зависимости от метода давления."""
 
@@ -70,10 +65,6 @@ class Person(AbstractNpc):
         else:
             return 'Я ничего не знаю...'
 
-    def update_relationship(self, change):
-        """Изменяет отношение NPC к инквизитору."""
-        self.relationship_with_inquisitor += change
-
     def __repr__(self):
         return str({
             'name': self.name,
@@ -91,64 +82,75 @@ npc_list = []
 
 def generate_npc() -> None:
     global npc_list
-    npc_list = [Person(i) for i in range(len(get_data('roles', 'npc')))]
-    assign_relationships()
+    npc_list = [Person(data={'is_new': True, 'npc_id': i}) for i in range(len(get_data('roles', 'npc')))]
+    assign_relationships(npc_list)
+
+def generate_loaded_npc(loaded_npc_list) -> None:
+    global npc_list
+    for npc in loaded_npc_list:
+        if npc['person_type'] == 'Citizen':
+            npc_list.append(Person(npc, False))
+        if npc['person_type'] == 'Accomplice':
+            npc_list.append(Accomplice(npc, False))
+        if npc['person_type'] == 'Ritualistic':
+            npc_list.append(Ritualistic(npc, False))
+        if npc['person_type'] == 'Possessed':
+            npc_list.append(Possessed(npc, False))
+        if npc['person_type'] == 'Avenger':
+            npc_list.append(Avenger(npc, False))
+        if npc['person_type'] == 'Accidental':
+            npc_list.append(Accidental(npc, False))
+        if npc['person_type'] == 'Helper':
+            npc_list.append(Helper(npc, False))
+
+    print(npc_list)
 
 def get_npc_list() -> npc_list:
     return npc_list
 
 # Assign relationships
-def assign_relationships() -> None:
+def assign_relationships(npc_list) -> None:
     random.shuffle(npc_list)
 
-    # Assign main roles
-    main_roles = [_('Victim'), _('Killer')]
-    main_npcs = random.sample(npc_list, 2)
-    murderer = None
-    victim = None
-
-    for i in range(len(main_roles)):
-        main_npcs[i].set_relationships({'role': main_roles[i]})
-        if main_roles[i] == _('Killer'):
-            murderer = main_npcs[i]
-            murderer.murderer_info = assign_murderer_type(murderer)
-        else:
-            victim = main_npcs[i]
+    npc_list[0] = assign_murderer_type(npc_list[0].__dict__.copy())
+    npc_list[0].set_relationships({'role': 'Murderer'})
+    npc_list[1].set_relationships({'role': 'Victim'})
 
     for npc in npc_list:
-        npc.known_clues = murderer.murderer_info.clues['PublicClues']
+        npc.known_clues = npc_list[0].clues['PublicClues']
 
     # Assign 2 accomplices, 3 helpers, and 2 neutrals
-    accomplices = random.sample([npc for npc in npc_list if npc not in main_npcs], 2)
-    helpers = random.sample([npc for npc in npc_list if npc not in accomplices and npc not in main_npcs], 3)
-    neutral_npcs = [npc for npc in npc_list if npc not in accomplices and npc not in helpers and npc not in main_npcs]
+    accomplices = npc_list[2:4]
+    helpers = npc_list[4:7]
+    neutral_npcs = npc_list[7:]
 
     # Set connections
-    for accomplice in accomplices:
+    for index, accomplice in enumerate(accomplices):
+        accomplice = assign_accomplice_type(accomplice.__dict__.copy(), npc_list[0].__dict__.copy())
         accomplice.set_relationships(
             {
                 'role': _('Accomplice'),
-                'knows_about': [murderer.name],
-                'victim_name': victim.name,
-                'victim_role': victim.role
+                'murderer_name': [npc_list[0].name],
+                'victim_name': npc_list[1].name,
+                'victim_role': npc_list[1].role
             })
-        accomplice.accomplice_info = assign_accomplice_type(accomplice, murderer)
+        npc_list[index+2] = accomplice
     for index, helper in enumerate(helpers):
+        clue = npc_list[0].clues['SecretClues'][index]
+        helper = assign_helper_type(helper.__dict__.copy(), clue=clue)
         helper.set_relationships(
             {
                 'role': _('Helper'),
-                'knows_about': [victim.name],
-                'victim_name': victim.name,
-                'victim_role': victim.role
+                'victim_name': npc_list[1].name,
+                'victim_role': npc_list[1].role
             })
-        clue = murderer.murderer_info.clues['SecretClues'][index]
-        helper.helper_info = assign_helper_type(helper, clue=clue)
+        npc_list[index + 4] = helper
     for neutral in neutral_npcs:
         neutral.set_relationships(
             {
                 'role': _('Neutral'),
-                'victim_name': victim.name,
-                'victim_role': victim.role
+                'victim_name': npc_list[1].name,
+                'victim_role': npc_list[1].role
             })
 
 def get_npc(role: str) -> Person or None:
