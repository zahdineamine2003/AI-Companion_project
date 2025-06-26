import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from ui.avatar_setup import AvatarSetupWidget
from ui.chat_window import ChatWindow

class WelcomePage(QWidget):
    def __init__(self, on_start):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel('🤗 <b>Welcome to AI Companion</b>')
        title.setFont(QFont('Arial', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel('Your caring, empathetic AI friend for support and wellness.')
        subtitle.setFont(QFont('Arial', 16))
        subtitle.setAlignment(Qt.AlignCenter)
        start_btn = QPushButton('Get Started')
        start_btn.setFixedWidth(200)
        start_btn.setStyleSheet('font-size:18px; padding:12px;')
        start_btn.clicked.connect(on_start)
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(subtitle)
        layout.addSpacing(40)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class Sidebar(QWidget):
    def __init__(self, avatar_path, name, on_nav):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Avatar
        avatar = QLabel()
        pixmap = QPixmap(avatar_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar.setPixmap(pixmap)
        avatar.setAlignment(Qt.AlignCenter)
        layout.addWidget(avatar)
        # Name
        name_label = QLabel(f'<b>{name}</b>')
        name_label.setFont(QFont('Arial', 14))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        layout.addSpacing(30)
        # Navigation
        self.list = QListWidget()
        self.list.setIconSize(pixmap.size())
        self.list.addItem(QListWidgetItem(QIcon(':/icons/chat.png'), 'Chat'))
        self.list.addItem(QListWidgetItem(QIcon(':/icons/avatar.png'), 'Avatar'))
        self.list.setCurrentRow(0)
        self.list.currentRowChanged.connect(on_nav)
        layout.addWidget(self.list)
        layout.addStretch()
        self.setLayout(layout)
        self.setFixedWidth(120)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Companion - Cyber Friend')
        self.setGeometry(100, 100, 900, 700)
        self.user_info = {'name': 'Your Friend', 'avatar': 'assets/avatars/male1.png'}
        self.init_ui()

    def init_ui(self):
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QHBoxLayout(self.central)
        # Stacked pages
        self.pages = QStackedWidget()
        self.welcome_page = WelcomePage(self.show_avatar_setup)
        self.avatar_page = AvatarSetupWidget(on_continue=self.on_avatar_setup_complete)
        self.chat_page = ChatWindow(user_info=self.user_info)
        self.pages.addWidget(self.welcome_page)
        self.pages.addWidget(self.avatar_page)
        self.pages.addWidget(self.chat_page)
        # Sidebar (initially hidden)
        self.sidebar = None
        self.main_layout.addWidget(self.pages)
        self.setStyleSheet(self.get_stylesheet())

    def show_avatar_setup(self):
        self.pages.setCurrentIndex(1)

    def on_avatar_setup_complete(self, user_info):
        self.user_info = user_info
        # Update sidebar
        if self.sidebar:
            self.main_layout.removeWidget(self.sidebar)
            self.sidebar.deleteLater()
        avatar_path = f"assets/avatars/{user_info['avatar']}"
        self.sidebar = Sidebar(avatar_path, user_info['name'], self.on_nav)
        self.main_layout.insertWidget(0, self.sidebar)
        # Update chat page
        self.chat_page = ChatWindow(user_info=user_info)
        self.pages.removeWidget(self.pages.widget(2))
        self.pages.addWidget(self.chat_page)
        self.pages.setCurrentIndex(2)

    def on_nav(self, idx):
        # 0: Chat, 1: Avatar
        self.pages.setCurrentIndex(idx+2 if idx else 2)

    def get_stylesheet(self):
        return '''
        QMainWindow { background: #f6f8fa; }
        QLabel { color: #22223b; }
        QPushButton { background: #43b581; color: #fff; border-radius: 8px; padding: 10px 20px; font-size: 16px; }
        QPushButton:hover { background: #23855c; }
        QListWidget { background: #e3e5e8; border: none; font-size: 16px; }
        QListWidget::item:selected { background: #43b581; color: #fff; border-radius: 8px; }
        QWidget#ChatBubbleUser { background: #43b581; color: #fff; border-radius: 16px; padding: 8px 16px; }
        QWidget#ChatBubbleAI { background: #e3e5e8; color: #22223b; border-radius: 16px; padding: 8px 16px; }
        '''

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 