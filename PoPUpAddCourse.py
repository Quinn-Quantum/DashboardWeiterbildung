from PyQt6.QtWidgets import (
     QDialog, QLineEdit,
    QPushButton, QRadioButton, QVBoxLayout, QLabel, QComboBox
)

from TestTypes import TestTypes


class PoPUpAddCourse(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kurs eintragen")
        self.resize(300, 350)

        # Layout für das Pop-up
        layout = QVBoxLayout()
        #label for course name
        layout.addWidget(QLabel("Kurs Name"))
        # input course
        self.course_name = QLineEdit(self)
        layout.addWidget(self.course_name)

        # label test
        layout.addWidget(QLabel("Prüfungsartart"))
        # input test
        self.test_name = QComboBox(self)
        for test in TestTypes:
            self.test_name.addItem(test.value, test)
        layout.addWidget(self.test_name)

        # label mandatorily
        layout.addWidget(QLabel("Ist die Prüfung verpflichtent?"))

        # radio button for mandatorily
        self.radio_one = QRadioButton("Verpflichtende Prüfung", self)
        self.radio_two = QRadioButton("Freiwillige Prüfung", self)
        self.radio_one.setChecked(True)  # Standard option is mandatorily selected

        layout.addWidget(self.radio_one)
        layout.addWidget(self.radio_two)

        # submit
        self.btn_ok = QPushButton("OK", self)
        self.btn_ok.setStyleSheet("background-color: rgb(110, 53, 201); color: white; padding: 6px;")
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def get_selected_test_type(self):
        """Return the selected test type"""
        return self.test_name.currentText() # currentText() returns the String from the Enum