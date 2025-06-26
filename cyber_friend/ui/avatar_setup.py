from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QGroupBox, QGridLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os

class AvatarSetupWidget(QWidget):
    def __init__(self, on_continue=None):
        super().__init__()
        self.on_continue = on_continue
        self.selected_gender = 'male'
        self.selected_avatar = 'male1.png'
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h2>Set Up Your AI Companion</h2>'))

        # Gender selection
        gender_group = QGroupBox('Choose Gender')
        gender_layout = QHBoxLayout()
        self.male_radio = QRadioButton('Male')
        self.female_radio = QRadioButton('Female')
        self.male_radio.setChecked(True)
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_group.setLayout(gender_layout)
        layout.addWidget(gender_group)

        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel('Name:'))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter a name for your companion')
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Avatar selection (placeholder images)
        avatar_group = QGroupBox('Choose Avatar')
        avatar_layout = QGridLayout()
        self.avatar_buttons = []
        self.avatar_images = ['male1.png', 'female1.png']
        for i, img in enumerate(self.avatar_images):
            btn = QPushButton()
            btn.setCheckable(True)
            if i == 0:
                btn.setChecked(True)
            pixmap = QPixmap(os.path.join('assets', 'avatars', img)).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.clicked.connect(lambda checked, idx=i: self.select_avatar(idx))
            self.avatar_buttons.append(btn)
            avatar_layout.addWidget(btn, 0, i)
        avatar_group.setLayout(avatar_layout)
        layout.addWidget(avatar_group)

        # Continue button
        self.continue_btn = QPushButton('Continue')
        self.continue_btn.clicked.connect(self.handle_continue)
        layout.addWidget(self.continue_btn)

        self.setLayout(layout)

        # Connect gender radio buttons
        self.male_radio.toggled.connect(self.update_gender)
        self.female_radio.toggled.connect(self.update_gender)

    def update_gender(self):
        if self.male_radio.isChecked():
            self.selected_gender = 'male'
            self.select_avatar(0)
        else:
            self.selected_gender = 'female'
            self.select_avatar(1)

    def select_avatar(self, idx):
        for i, btn in enumerate(self.avatar_buttons):
            btn.setChecked(i == idx)
        self.selected_avatar = self.avatar_images[idx]

    def handle_continue(self):
        name = self.name_input.text().strip()
        if not name:
            self.name_input.setPlaceholderText('Please enter a name!')
            return
        if self.on_continue:
            self.on_continue({
                'gender': self.selected_gender,
                'name': name,
                'avatar': self.selected_avatar
            }) 