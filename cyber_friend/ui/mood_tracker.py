from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QDate
from core.database import Database

class MoodTrackerWidget(QWidget):
    def __init__(self, on_submit=None):
        super().__init__()
        self.on_submit = on_submit
        self.selected_mood = None
        self.moods = [
            ("😄", "Happy"),
            ("🙂", "Okay"),
            ("😐", "Neutral"),
            ("😔", "Sad"),
            ("😠", "Angry")
        ]
        self.db = Database()
        self.init_ui()
        self.update_summary()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h2>How are you feeling today?</h2>'))

        mood_layout = QHBoxLayout()
        self.mood_buttons = []
        for emoji, label in self.moods:
            btn = QPushButton(emoji)
            btn.setCheckable(True)
            btn.setFixedSize(48, 48)
            btn.clicked.connect(lambda checked, l=label: self.select_mood(l))
            self.mood_buttons.append(btn)
            mood_layout.addWidget(btn)
        layout.addLayout(mood_layout)

        self.submit_btn = QPushButton('Submit Mood')
        self.submit_btn.clicked.connect(self.submit_mood)
        layout.addWidget(self.submit_btn)

        # Weekly summary
        self.summary_label = QLabel('')
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def select_mood(self, label):
        self.selected_mood = label
        for btn, (_, l) in zip(self.mood_buttons, self.moods):
            btn.setChecked(l == label)

    def submit_mood(self):
        if not self.selected_mood:
            QMessageBox.warning(self, 'No Mood Selected', 'Please select your mood before submitting.')
            return
        today = QDate.currentDate().toString(Qt.ISODate)
        self.db.save_mood(today, self.selected_mood)
        if self.on_submit:
            self.on_submit({
                'date': today,
                'mood': self.selected_mood
            })
        QMessageBox.information(self, 'Mood Saved', f"Your mood ({self.selected_mood}) has been saved!")
        self.update_summary()

    def update_summary(self):
        moods = self.db.get_moods(limit=7)
        if not moods:
            self.summary_label.setText('<i>No mood data for the past week.</i>')
            return
        summary = 'Last 7 days:\n'
        for date, mood in reversed(moods):
            summary += f'{date}: {mood}\n'
        self.summary_label.setText(summary) 