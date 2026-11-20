
from PyQt6.QtWidgets import (
     QDialog, QLineEdit,
     QRadioButton, QVBoxLayout, QLabel, QComboBox
)

from TestTypes import TestTypes
from button_helper import ok_button

class PoPUpAddCourse(QDialog):

    def __init__(
            self,
            parent=None,
            course_id: int | None = None,
            course_name: str = "",
            test_type_of_examination=None,
            test_is_mandatory: bool = True,
    ):
        super().__init__(parent)
        self.course_id = course_id
        self.is_edit_mode = course_id is not None
        self.setWindowTitle("Kurs bearbeiten" if self.is_edit_mode else "Kurs eintragen")
        self.resize(300, 350)

        # Layout for Pop-up
        layout = QVBoxLayout()
        self.course_name = QLineEdit(course_name or "", self)
        layout.addWidget(self.course_name)

        layout.addWidget(QLabel("Prüfungsart"))
        self.test_name = QComboBox(self)
        for test in TestTypes:
            self.test_name.addItem(test.value, test)
        layout.addWidget(self.test_name)

        layout.addWidget(QLabel("Ist die Prüfung verpflichtend?"))
        self.radio_one = QRadioButton("Verpflichtende Prüfung", self)
        self.radio_two = QRadioButton("Freiwillige Prüfung", self)
        layout.addWidget(self.radio_one)
        layout.addWidget(self.radio_two)

        self.btn_ok = ok_button(self, on_click=self.accept)
        layout.addWidget(self.btn_ok)


    def get_selected_test_type(self):
        """Return the selected test type"""
        return self.test_name.currentText() # currentText() returns the String from the Enum

    def _set_selected_test_type(self, value) -> None:
        if value is None:
            return
        if not isinstance(value, TestTypes):
            # Falls in der DB der Enum-Wert (z. B. "Klausur") oder der Name (z. B. "EXAM") steht:
            try:
                value = TestTypes(value)
            except ValueError:
                value = TestTypes[str(value)]

        index = self.test_name.findData(value)
        if index != -1:
            self.test_name.setCurrentIndex(index)

    def _set_mandatory_radio(self, is_mandatory: bool) -> None:
        if is_mandatory:
            self.radio_one.setChecked(True)
        else:
            self.radio_two.setChecked(True)