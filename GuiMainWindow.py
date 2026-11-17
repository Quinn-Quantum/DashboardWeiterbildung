from PyQt6 import QtCore, QtWidgets

class GuiMainWindow(object):

    def setup_ui(self, Dialog):
        Dialog.setObjectName("Plan")
        Dialog.resize(1062, 720)

        # 1. Create a central widget for the QMainWindow
        self.central_widget = QtWidgets.QWidget(parent=Dialog)
        self.central_widget.setObjectName("central_widget")

        # 2. Set the main layout to the central widget
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # --- First line: Labels at the top ---
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.aktiv_label = QtWidgets.QLabel(parent=self.central_widget)
        self.aktiv_label.setObjectName("aktiv_label")
        self.horizontalLayout.addWidget(self.aktiv_label)

        self.calender_label = QtWidgets.QLabel(parent=self.central_widget)
        self.calender_label.setObjectName("calender_label")
        self.horizontalLayout.addWidget(self.calender_label)

        self.main_layout.addLayout(self.horizontalLayout)

        # --- Second line: aktiv course and calendar ---
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        # HIER GEÄNDERT: QWidget statt QColumnView als Container verwenden!
        self.active_course_container = QtWidgets.QWidget(parent=self.central_widget)
        self.active_course_container.setObjectName("active_course_container")

        self.active_course_layout = QtWidgets.QVBoxLayout(self.active_course_container)
        self.active_course_layout.setContentsMargins(0, 0, 0, 0)

        self.active_course_placeholder = QtWidgets.QLabel("Kein Kurs ausgewählt", parent=self.active_course_container)
        self.active_course_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.active_course_placeholder.setMinimumHeight(120)
        self.active_course_placeholder.setStyleSheet("""
                    QLabel {
                        color: #888;
                        font-style: italic;
                        background-color: #f8f9fa;
                        border: 2px dashed #dee2e6;
                        border-radius: 10px;
                    }
                """)
        self.active_course_layout.addWidget(self.active_course_placeholder)

        self.horizontalLayout_2.addWidget(self.active_course_container)

        self.calendarWidget = QtWidgets.QCalendarWidget(parent=self.central_widget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setMinimumSize(QtCore.QSize(400, 300))
        self.horizontalLayout_2.addWidget(self.calendarWidget)

        self.main_layout.addLayout(self.horizontalLayout_2)

        # --- Third line: Course label and add button ---
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.kurs_label = QtWidgets.QLabel(parent=self.central_widget)
        self.kurs_label.setObjectName("kurs_label")
        self.horizontalLayout_3.addWidget(self.kurs_label)

        self.horizontalLayout_3.addStretch()

        self.add_button = QtWidgets.QPushButton("open add course", parent=self.central_widget)
        self.add_button.setStyleSheet("background-color: rgb(110, 53, 201); color: white;")
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_3.addWidget(self.add_button)

        self.main_layout.addLayout(self.horizontalLayout_3)

        # --- Fourth row: Table ---
        self.kurs_listWidget = QtWidgets.QListWidget(parent=self.central_widget)
        self.kurs_listWidget.setObjectName("kurs_listWidget")
        self.kurs_listWidget.setStyleSheet("QListWidget { background: transparent; border: none; }")
        self.main_layout.addWidget(self.kurs_listWidget)

        # Pass the central widget to the QMainWindow
        Dialog.setCentralWidget(self.central_widget)

        self.retranslate_ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Planer"))
        self.aktiv_label.setText(_translate("Dialog", "Aktueller Kurs"))
        self.calender_label.setText(_translate("Dialog", "Kalender"))
        self.kurs_label.setText(_translate("Dialog", "Kurse"))
        self.add_button.setText(_translate("Dialog", "Add"))