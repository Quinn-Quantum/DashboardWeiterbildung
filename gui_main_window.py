from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1062, 720)

        # 1. Zentrales Widget für das QMainWindow erstellen
        self.central_widget = QtWidgets.QWidget(parent=Dialog)
        self.central_widget.setObjectName("central_widget")

        # 2. Das Hauptlayout auf das zentrale Widget setzen
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # --- Erste Zeile: Labels oben ---
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.aktiv_label = QtWidgets.QLabel(parent=self.central_widget)
        self.aktiv_label.setObjectName("aktiv_label")
        self.horizontalLayout.addWidget(self.aktiv_label)

        self.calender_label = QtWidgets.QLabel(parent=self.central_widget)
        self.calender_label.setObjectName("calender_label")
        self.horizontalLayout.addWidget(self.calender_label)

        self.main_layout.addLayout(self.horizontalLayout)

        # --- Zweite Zeile: ColumnView und Kalender ---
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        self.columnView = QtWidgets.QColumnView(parent=self.central_widget)
        self.columnView.setObjectName("columnView")
        self.horizontalLayout_2.addWidget(self.columnView)

        self.calendarWidget = QtWidgets.QCalendarWidget(parent=self.central_widget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setMinimumSize(QtCore.QSize(400, 300))
        self.horizontalLayout_2.addWidget(self.calendarWidget)

        self.main_layout.addLayout(self.horizontalLayout_2)

        # --- Dritte Zeile: Kurs-Label und Add-Button ---
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.kurs_label = QtWidgets.QLabel(parent=self.central_widget)
        self.kurs_label.setObjectName("kurs_label")
        self.horizontalLayout_3.addWidget(self.kurs_label)

        self.horizontalLayout_3.addStretch()

        self.add_button = QtWidgets.QPushButton(parent=self.central_widget)
        self.add_button.setStyleSheet("background-color: rgb(110, 53, 201); color: white;")
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_3.addWidget(self.add_button)

        self.main_layout.addLayout(self.horizontalLayout_3)

        # --- Vierte Zeile: Tabelle ---
        self.kurs_tableView = QtWidgets.QTableView(parent=self.central_widget)
        self.kurs_tableView.setObjectName("kurs_tableView")
        self.main_layout.addWidget(self.kurs_tableView)

        # 3. Dem QMainWindow das zentrale Widget übergeben
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