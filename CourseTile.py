from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class CourseTile(QFrame):
    def __init__(self, course_id, name, test_name, is_mandatory, parent=None):
        super().__init__(parent)
        self.course_id = course_id
        self.name = name          # <--- HIER MUSS DAS HIN
        self.test_name = test_name  # <--- UND HIER
        self.is_mandatory = is_mandatory # <--- Optional, aber gut zu haben
        self.is_active = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(80)
        self.setStyleSheet("""
                    CourseTile {
                        background-color: #f8f9fa;
                        border: 2px solid #dee2e6;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    CourseTile:hover {
                        border-color: #6e35c9;
                    }
                """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.name_label = QLabel(f"<b>Kurs:</b> {name}")
        self.name_label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(self.name_label)

        mandatory_text = "Verpflichtend" if is_mandatory else "Freiwillig"
        self.info_label = QLabel(f"<b>Prüfung:</b> {test_name} ({mandatory_text})")
        self.info_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.info_label)

    def set_active_style(self, active: bool):
        self.is_active = active
        if active:
            self.setStyleSheet("""
                        CourseTile {
                            background-color: #e6f0ff;
                            border: 2px solid #6e35c9;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    """)
        else:
            self.setStyleSheet("""
                        CourseTile {
                            background-color: #f8f9fa;
                            border: 2px solid #dee2e6;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    """)