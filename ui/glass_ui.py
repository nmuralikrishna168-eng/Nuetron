from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QTextEdit, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from config import USER_NAME, APP_TITLE, APP_MIN_WIDTH, APP_MIN_HEIGHT, OLLAMA_MODEL


class GlassCard(QFrame):
    """Custom frosted-glass card component with neon styling."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: rgba(18, 24, 45, 0.65);
                border: 1px solid rgba(0, 204, 255, 0.25);
                border-radius: 18px;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 150, 255, 40))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)


class NuetronMainWindow(QMainWindow):
    """Main NUETRON v16 application window with glassmorphism UI."""

    user_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #050814, stop:0.5 #0c1228, stop:1 #08031a
                );
            }
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)

        center_panel = self._create_center_panel()
        main_layout.addLayout(center_panel, stretch=5)

        right_panel = self._create_right_panel()
        main_layout.addLayout(right_panel, stretch=2)

    def _create_sidebar(self) -> QFrame:
        sidebar = GlassCard()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        brand = QLabel("NUETRON v16\nDesktop Assistant")
        brand.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        brand.setStyleSheet("color: #00d9ff; text-align: center;")
        sidebar_layout.addWidget(brand)
        sidebar_layout.addSpacing(25)

        nav_items = ["🏠 Home", "💬 Chat", "🎙️ Voice", "📁 Projects", "🔍 Search", "🧠 Memory", "⚙️ Settings"]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #b0c2de;
                    text-align: left;
                    font-size: 14px;
                    border: none;
                    padding: 10px;
                    border-radius: 8px;
                    margin: 2px 0px;
                }
                QPushButton:hover {
                    background: rgba(0, 217, 255, 0.15);
                    color: #ffffff;
                }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        user_info = QLabel(f"👤 {USER_NAME}\n● Pro User")
        user_info.setStyleSheet("color: #00ffaa; font-size: 12px; text-align: center;")
        sidebar_layout.addWidget(user_info)
        return sidebar

    def _create_center_panel(self) -> QVBoxLayout:
        center_panel = QVBoxLayout()
        center_panel.setSpacing(15)

        hero_card = GlassCard()
        hero_layout = QVBoxLayout(hero_card)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hero_title = QLabel("NUETRON v16")
        hero_title.setFont(QFont("Segoe UI", 26, QFont.Weight.ExtraBold))
        hero_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_title.setStyleSheet("color: #ffffff; letter-spacing: 2px;")

        hero_sub = QLabel(f"Think  •  Create  •  Automate\nGood Morning, {USER_NAME}")
        hero_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_sub.setStyleSheet("color: #a4b3d6; font-size: 14px;")

        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_sub)
        center_panel.addWidget(hero_card, stretch=2)

        self.display_box = QTextEdit()
        self.display_box.setReadOnly(True)
        self.display_box.setStyleSheet("""
            QTextEdit {
                background: rgba(8, 12, 28, 0.7);
                border: 1px solid rgba(0, 217, 255, 0.2);
                border-radius: 12px;
                color: #d1e2ff;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                padding: 12px;
            }
        """)
        center_panel.addWidget(self.display_box, stretch=4)

        input_card = GlassCard()
        input_layout = QHBoxLayout(input_card)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything... (voice or text)")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 15px;
                padding: 5px;
            }
        """)
        self.input_field.returnPressed.connect(self.handle_manual_submit)

        send_btn = QPushButton("🚀 Send")
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #0099ff, stop:1 #a200ff);
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #00ddff;
                color: black;
            }
        """)
        send_btn.clicked.connect(self.handle_manual_submit)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        center_panel.addWidget(input_card)
        return center_panel

    def _create_right_panel(self) -> QVBoxLayout:
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)

        status_card = GlassCard()
        status_layout = QVBoxLayout(status_card)

        status_title = QLabel("⚙️ System Status")
        status_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        status_title.setStyleSheet("color: #00d9ff;")
        status_layout.addWidget(status_title)

        status_info = QLabel("CPU: 18% | RAM: 42% | GPU: 12%")
        status_info.setStyleSheet("color: #a4b3d6; font-size: 11px;")
        status_layout.addWidget(status_info)

        self.status_lbl = QLabel("● Ready (Ollama: Online)")
        self.status_lbl.setStyleSheet("color: #00ffaa; font-weight: bold; font-size: 12px;")
        status_layout.addWidget(self.status_lbl)
        right_panel.addWidget(status_card)

        models_card = GlassCard()
        models_layout = QVBoxLayout(models_card)

        models_title = QLabel("⚡ AI Engines Active")
        models_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        models_title.setStyleSheet("color: #00d9ff;")
        models_layout.addWidget(models_title)

        engines = [
            "• Gemini 1.5 Pro: Active (Web Builder)",
            f"• Ollama ({OLLAMA_MODEL}): Ready (Local)",
            "• Screen Scanner Vision: Active"
        ]

        for engine in engines:
            engine_label = QLabel(engine)
            engine_label.setStyleSheet("color: #a4b3d6; font-size: 11px;")
            models_layout.addWidget(engine_label)

        right_panel.addWidget(models_card)
        right_panel.addStretch()
        return right_panel

    def append_log(self, sender: str, msg: str):
        self.display_box.append(f"<b style='color: #00d9ff;'>[{sender}]</b>: {msg}")

    def handle_manual_submit(self):
        text = self.input_field.text().strip()
        if text:
            self.append_log("USER", text)
            self.input_field.clear()
            self.user_submitted.emit(text)

    def update_status(self, status: str):
        self.status_lbl.setText(f"● {status}")

    def clear_display(self):
        self.display_box.clear()
