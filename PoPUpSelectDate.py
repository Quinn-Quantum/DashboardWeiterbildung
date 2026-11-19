from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCalendarWidget, QPushButton
from PyQt6.QtCore import QDate

from button_helper import ok_button


class PoPUpSelectDate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Startdatum wählen")
        self.resize(360, 380)

        layout = QVBoxLayout()

        self.label = QLabel("Wähle das Startdatum für den Kurs (4 Wochen):", self)
        layout.addWidget(self.label)

        # Use the QCalendarWidget directly instead of QDateEdit (prevents memory crashes)
        self.calendar = QCalendarWidget(self)
        self.calendar.setSelectedDate(QDate.currentDate())
        layout.addWidget(self.calendar)

        self.btn_ok = ok_button(self, on_click=self.accept)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def get_selected_date(self) -> QDate:
        """Returns the date selected directly in the calendar."""
        return self.calendar.selectedDate()