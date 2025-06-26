from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMessageBox

class VoiceWidget(QWidget):
    def __init__(self, on_tts=None, on_stt=None):
        super().__init__()
        self.on_tts = on_tts
        self.on_stt = on_stt
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.tts_btn = QPushButton('🔊 Read Aloud')
        self.tts_btn.clicked.connect(self.handle_tts)
        layout.addWidget(self.tts_btn)
        self.stt_btn = QPushButton('🎤 Record Speech')
        self.stt_btn.clicked.connect(self.handle_stt)
        layout.addWidget(self.stt_btn)
        self.setLayout(layout)

    def handle_tts(self):
        QMessageBox.information(self, 'TTS', 'Text-to-Speech coming soon!')
        if self.on_tts:
            self.on_tts()

    def handle_stt(self):
        QMessageBox.information(self, 'STT', 'Speech-to-Text coming soon!')
        if self.on_stt:
            self.on_stt() 