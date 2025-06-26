from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate
from core.database import Database

class JournalWidget(QWidget):
    def __init__(self, on_save=None):
        super().__init__()
        self.on_save = on_save
        self.db = Database()
        self.init_ui()
        self.load_today_entry()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h2>Daily Journal</h2>'))
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Write your thoughts or reflections here...')
        layout.addWidget(self.text_edit)
        self.save_btn = QPushButton('Save Entry')
        self.save_btn.clicked.connect(self.save_entry)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def load_today_entry(self):
        today = QDate.currentDate().toString()
        entry = self.db.get_journal(today)
        if entry:
            self.text_edit.setText(entry)
        else:
            self.text_edit.clear()

    def save_entry(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, 'Empty Entry', 'Please write something before saving.')
            return
        today = QDate.currentDate().toString()
        self.db.save_journal(today, text)
        if self.on_save:
            self.on_save({
                'date': today,
                'text': text
            })
        QMessageBox.information(self, 'Journal Saved', 'Your journal entry has been saved! (Encryption coming soon)') 