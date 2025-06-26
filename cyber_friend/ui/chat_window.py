from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from core.ai_chat import get_ai_response
import os

class ChatBubble(QWidget):
    def __init__(self, sender, message, is_user, avatar_path):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        if is_user:
            layout.addStretch()
        # Avatar
        avatar = QLabel()
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path).scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            avatar.setPixmap(pixmap)
        avatar.setFixedSize(36, 36)
        if is_user:
            layout.addWidget(avatar)
        # Bubble
        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setFont(QFont('Arial', 13))
        bubble.setObjectName('ChatBubbleUser' if is_user else 'ChatBubbleAI')
        bubble.setStyleSheet('QLabel#ChatBubbleUser { background: #43b581; color: #fff; border-radius: 16px; padding: 8px 16px; } QLabel#ChatBubbleAI { background: #e3e5e8; color: #22223b; border-radius: 16px; padding: 8px 16px; }')
        if is_user:
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addWidget(avatar)
            layout.addStretch()
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

class ChatWindow(QWidget):
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info or {'name': 'Your Friend', 'avatar': 'assets/avatars/male1.png'}
        self.messages = []  # Store chat context
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Chat area (scrollable)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
        # Input area
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('Type your message...')
        self.input_box.setFont(QFont('Arial', 13))
        self.send_btn = QPushButton('Send')
        self.send_btn.setFixedHeight(36)
        self.send_btn.setStyleSheet('font-size:15px;')
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)
        main_layout.addLayout(input_layout)

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return
        self.append_message('You', user_text, is_user=True)
        self.messages.append({"role": "user", "content": user_text})
        self.input_box.clear()
        # Get AI response
        ai_response = get_ai_response(self.messages, self.user_info)
        self.append_message(self.user_info.get('name', 'AI'), ai_response, is_user=False)
        self.messages.append({"role": "assistant", "content": ai_response})

    def append_message(self, sender, message, is_user):
        avatar_path = f"assets/avatars/{self.user_info['avatar']}" if not is_user else "assets/avatars/user.png"
        if is_user and not os.path.exists(avatar_path):
            avatar_path = "assets/avatars/male1.png"
        bubble = ChatBubble(sender, message, is_user, avatar_path)
        self.scroll_layout.addWidget(bubble)
        # Auto-scroll to bottom
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()) 