import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QTextCharFormat, QColor

from CourseTile import CourseTile
from Dashboard import Dashboard
from DatabaseConnection import DatabaseConnection
from GuiMainWindow import UiDialog
import PoPUpAddCourse


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Initialize Database and Dashboard
        self.db = DatabaseConnection()
        self.dashboard = Dashboard(self.db)

        # 2. Initialize UI class and apply it to the window
        self.ui = UiDialog()
        self.ui.setup_ui(self)

        # 3. Connect button click and list selection
        self.ui.add_button.clicked.connect(self.open_popup)
        self.ui.kurs_listWidget.itemClicked.connect(self.select_active_course)

        # Setup calendar & load courses
        self.time_for_study = self.dashboard.lade_time()
        self.setup_calendar_periods()
        self.refresh_course_tiles()

    def open_popup(self):
        dialog = PoPUpAddCourse.PoPUpAddCourse(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name_course = dialog.course_name.text()
            test_name = dialog.test_name.text()
            is_mandatory = dialog.radio_one.isChecked()

            self.dashboard.store_in_db(name_course, test_name, is_mandatory)
            self.refresh_course_tiles()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

    def refresh_course_tiles(self):
        """Lädt Kurse und stellt den gespeicherten aktiven Kurs beim Start wieder her."""
        self.ui.kurs_listWidget.clear()
        courses = self.dashboard.load_courses_from_db()

        active_tile_to_restore = None

        for course_data in courses:
            c_id, name, time, test_name, is_mandatory, is_active = course_data
            tile = CourseTile(c_id, name, test_name, is_mandatory)

            item = QListWidgetItem(self.ui.kurs_listWidget)
            item.setSizeHint(tile.sizeHint())
            self.ui.kurs_listWidget.setItemWidget(item, tile)

            # Wenn dieser Kurs in der DB als aktiv markiert ist, merken wir ihn uns
            if is_active == 1:
                active_tile_to_restore = tile

        # Falls ein aktiver Kurs gefunden wurde, UI direkt darauf einstellen
        if active_tile_to_restore:
            self.activate_course(active_tile_to_restore)

    def select_active_course(self, item):
        """Wird aufgerufen, wenn der Benutzer manuell auf eine Kachel klickt."""
        clicked_tile = self.ui.kurs_listWidget.itemWidget(item)
        if clicked_tile:
            # In Datenbank speichern
            self.dashboard.set_aktive_course(clicked_tile.course_id)
            # UI aktualisieren
            self.activate_course(clicked_tile)

    def activate_course(self, active_tile):
        """Zentrale Methode, um eine Kachel als aktiv darzustellen und den Kalender zu aktualisieren."""
        for i in range(self.ui.kurs_listWidget.count()):
            it = self.ui.kurs_listWidget.item(i)
            tile = self.ui.kurs_listWidget.itemWidget(it)

            if tile == active_tile:
                tile.set_active_style(True)

                # Alten aktiven Eintrag im oberen Bereich entfernen
                while self.ui.active_course_layout.count():
                    child = self.ui.active_course_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                # Neue aktive Kachel in Lila/Weiß erstellen
                active_display_tile = CourseTile(tile.course_id, tile.name, tile.test_name, tile.is_mandatory)
                active_display_tile.setStyleSheet("""
                    CourseTile {
                        background-color: #6e35c9;
                        border: 2px solid #522596;
                        border-radius: 10px;
                        padding: 15px;
                    }
                """)
                active_display_tile.name_label.setStyleSheet("font-size: 15px; color: white;")
                active_display_tile.info_label.setStyleSheet("font-size: 13px; color: #f0e6ff;")

                self.ui.active_course_layout.addWidget(active_display_tile)
                active_display_tile.show()

                self.ui.aktiv_label.setText(f"Aktueller Kurs: {tile.name}")
                print(f"Aktiver Kurs geladen/aktiviert: ID {tile.course_id} ({tile.name})")

                self.highlight_course_duration(QDate.currentDate())
            else:
                tile.set_active_style(False)

    def setup_calendar_periods(self):
        current_year = QDate.currentDate().year()
        start_date = QDate(current_year, 10, 19)
        end_date = start_date.addMonths(6)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#e2e8f0"))

        d = start_date
        while d <= end_date:
            self.ui.calendarWidget.setDateTextFormat(d, fmt)
            d = d.addDays(1)

    def highlight_course_duration(self, start_date: QDate):
        self.setup_calendar_periods()
        end_date = start_date.addDays(28)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#6e35c9"))
        fmt.setForeground(QColor("white"))

        d = start_date
        while d <= end_date:
            self.ui.calendarWidget.setDateTextFormat(d, fmt)
            d = d.addDays(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())