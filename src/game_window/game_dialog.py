from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QVBoxLayout, QLabel, QLineEdit
from src.translation.translation import _

class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(_('Do you want create new game?'))
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class LoadGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(_('Do you want to load game?'))
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class SaveGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.new_save_name = ''
        self.setWindowTitle(_('Save game'))

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        line_edit = QLineEdit()
        line_edit.textEdited.connect(self.text_edited)
        message = QLabel(_('Please enter name of save'))
        layout.addWidget(message)
        layout.addWidget(line_edit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def text_edited(self, s):
        self.new_save_name = s

    def accept(self):
        if self.new_save_name:
            super().accept()