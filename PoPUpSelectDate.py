from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCalendarWidget, QPushButton
from PyQt6.QtCore import QDate

class PoPUpSelectDate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Startdatum wählen")
        self.resize(360, 380)

        layout = QVBoxLayout()

        self.label = QLabel("Wähle das Startdatum für den Kurs (4 Wochen):", self)
        layout.addWidget(self.label)

        # Verwende direkt den QCalendarWidget statt QDateEdit (verhindert den Speicherabsturz)
        self.calendar = QCalendarWidget(self)
        self.calendar.setSelectedDate(QDate.currentDate())
        layout.addWidget(self.calendar)

        self.btn_ok = QPushButton("OK", self)
        self.btn_ok.setStyleSheet("background-color: rgb(110, 53, 201); color: white; padding: 6px;")
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def get_selected_date(self) -> QDate:
        """Gibt das direkt im Kalender ausgewählte Datum zurück."""
        return self.calendar.selectedDate()