from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class CourseTile(QFrame):
    delete_requested = pyqtSignal(int)

    def __init__(self, course_id, name, test_name, is_mandatory, is_complete=0, parent=None):
        super().__init__(parent)
        self.course_id = course_id
        self.name = name
        self.test_name = test_name
        self.is_mandatory = is_mandatory
        self.is_complete = is_complete
        self.is_active = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(80)

        # Main Layout (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Top Panel: Horizontal Layout for Course Name and Delete Buttton
        top_layout = QHBoxLayout()

        self.name_label = QLabel(f"<b>Course:</b> {name}")
        self.name_label.setStyleSheet("font-size: 14px; color: #333;")
        top_layout.addWidget(self.name_label)

        top_layout.addStretch()

        # Delete button
        self.delete_btn = QPushButton("❌", self)
        self.delete_btn.setFixedSize(30, 30)
        # IMPORTANT: Prevents the ListWidget from swallowing the button's click
        self.delete_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #ff4d4d;
            }
            QPushButton:hover {
                background-color: #ffeeee;
                border-radius: 15px;
            }
        """)

        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.course_id))

        top_layout.addWidget(self.delete_btn)
        main_layout.addLayout(top_layout)

        if self.is_complete == 1:
            self.info_label = QLabel(f"<b>Komplett</b>)")
            self.info_label.setStyleSheet("font-size: 12px; color: #666;")
        else:
            mandatory_text = "Verpflichtend" if is_mandatory else "Freiwillig"
            self.info_label = QLabel(f"<b>Prüfung:</b> {test_name} ({mandatory_text})")
            self.info_label.setStyleSheet("font-size: 12px; color: #666;")

        main_layout.addWidget(self.info_label)

        self.update_style()

    def set_active_style(self, active: bool):
        self.is_active = active
        self.update_style()

    def update_style(self):
        if self.is_active:
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