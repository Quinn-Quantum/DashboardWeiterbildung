from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDateEdit, QSpinBox, QPushButton
from PyQt6.QtCore import QDate

class PoPUpSetup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weiterbildung Starten")
        self.resize(320, 220)

        layout = QVBoxLayout()

        self.label_info = QLabel("Willkommen! Bitte gib die Eckdaten deiner Weiterbildung ein. (Standart ist Heute und 6 Monate)", self)
        self.label_info.setWordWrap(True)
        layout.addWidget(self.label_info)

        layout.addWidget(QLabel("Startdatum der Weiterbildung:"))
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Gesamtdauer in Monaten:"))
        self.spin_months = QSpinBox(self)
        self.spin_months.setRange(1, 60)
        self.spin_months.setValue(6)  # default 6 months
        layout.addWidget(self.spin_months)

        self.btn_submit = QPushButton("Speichern", self)
        self.btn_submit.setStyleSheet("background-color: rgb(110, 53, 201); color: white; padding: 8px; font-weight: bold;")
        self.btn_submit.clicked.connect(self.accept)
        layout.addWidget(self.btn_submit)

        self.setLayout(layout)

    def get_setup_data(self):
        """Returns the start date as a string and the months."""
        start_date_str = self.date_edit.date().toString("yyyy-MM-dd")
        months = self.spin_months.value()
        return start_date_str, months