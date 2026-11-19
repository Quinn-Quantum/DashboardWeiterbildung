from PyQt6.QtWidgets import (
     QDialog,
    QPushButton, QRadioButton, QVBoxLayout, QLabel
)

from button_helper import ok_button


class PopUpCourseComplete(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kurs Komplet")
        self.resize(360, 380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # radio button for mandatorily
        self.label = QLabel("Möchtest du den Kurs als komplett markieren?", self)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        self.radio_one = QRadioButton("Ja, Kurs ist komplett", self)
        self.radio_two = QRadioButton("Nein, noch nicht", self)
        self.radio_one.setChecked(True)  # Standard option is mandatorily selected
        layout.addWidget(self.radio_one)
        layout.addWidget(self.radio_two)

        layout.addStretch()

        self.btn_ok = ok_button(self, on_click=self.accept)
        layout.addWidget(self.btn_ok)