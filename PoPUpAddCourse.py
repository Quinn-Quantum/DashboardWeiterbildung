import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QRadioButton, QVBoxLayout, QWidget
)


class PoPUpAddCourse(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kurs eintragen")
        self.resize(250, 150)

        # Layout für das Pop-up
        layout = QVBoxLayout()

        self.course_name = QLineEdit(self)
        self.course_name.setPlaceholderText("Kurs Name: ")
        layout.addWidget(self.course_name)

        self.test_name = QLineEdit(self)
        self.test_name.setPlaceholderText("Test Art eintragen: ")
        layout.addWidget(self.test_name)

        self.radio_one = QRadioButton("Verpflichtender Test", self)
        self.radio_two = QRadioButton("Freiwilliger Test", self)
        self.radio_one.setChecked(True)  # Standardmäßig Option A auswählen

        layout.addWidget(self.radio_one)
        layout.addWidget(self.radio_two)

        self.btn_ok = QPushButton("OK", self)
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)