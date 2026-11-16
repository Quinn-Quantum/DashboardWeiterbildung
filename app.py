import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QTextCharFormat, QColor

from CourseTile import CourseTile
from Dashboard import Dashboard
from DatabaseConnection import DatabaseConnection
from GuiMainWindow import UiDialog
import PoPUpAddCourse
from PoPUpSelectDate import PoPUpSelectDate

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
        dialog =PoPUpAddCourse.PoPUpAddCourse(self)
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
        """Loads courses and restores the saved active course at startup."""
        self.ui.kurs_listWidget.clear()
        self.ui.kurs_listWidget.clear()
        courses = self.dashboard.load_courses_from_db()

        active_tile_to_restore = None
        active_start_date = None

        for course_data in courses:
            c_id, name, time, test_name, is_mandatory, is_active, start_date = course_data
            tile = CourseTile(c_id, name, test_name, is_mandatory)

            tile.delete_requested.connect(self.delete_course_action)

            item = QListWidgetItem(self.ui.kurs_listWidget)
            item.setSizeHint(tile.sizeHint())
            self.ui.kurs_listWidget.setItemWidget(item, tile)

            # If this course is marked as active in the DB, we will remember it
            if is_active == 1:
                active_tile_to_restore = tile
                if start_date:
                    active_start_date = QDate.fromString(start_date, "yyyy-MM-dd")
                else:
                    active_start_date = QDate.currentDate()

        # If an active course is found, set the UI directly to it
        if active_tile_to_restore:
            self.activate_course(active_tile_to_restore, active_start_date)

    def select_active_course(self, item):
        """Called when the user manually clicks on a tile."""
        clicked_tile = self.ui.kurs_listWidget.itemWidget(item)
        if clicked_tile:
            self.is_dialog_open = True
            try:
                date_dialog = PoPUpSelectDate(None)
                if date_dialog.exec() == QDialog.DialogCode.Accepted:
                    selected_date = date_dialog.get_selected_date()
                    date_str = selected_date.toString("yyyy-MM-dd")

                    # Save to database
                    self.dashboard.set_aktive_course(clicked_tile.course_id, date_str)
                    # Update UI & Calendar
                    self.activate_course(clicked_tile, selected_date)
            except Exception as e:
                print("PopUp for the start date: ", e)
            finally:
                self.is_dialog_open = False

    def activate_course(self, active_tile, start_date: QDate):
        """Central way to make a tile active and update the calendar."""
        for i in range(self.ui.kurs_listWidget.count()):
            it = self.ui.kurs_listWidget.item(i)
            tile = self.ui.kurs_listWidget.itemWidget(it)

            if tile.course_id == active_tile.course_id:
                tile.set_active_style(True)

                # Remove old active entry at the top
                while self.ui.active_course_layout.count():
                    child = self.ui.active_course_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                # New Active Tile
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

                self.ui.aktiv_label.setText(f"Current Course: {tile.name} (Start: {start_date.toString('dd.MM.yyyy')})")
                print(f"Current Course loaded/activated: ID {tile.course_id} ({tile.name}) ab {start_date.toString('yyyy-MM-dd')}")

                self.highlight_course_duration(start_date)
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

    def delete_course_action(self, course_id):
        """Called when the X in a tile is clicked."""
        # Delete from DB
        self.dashboard.delete_course(course_id)

        # Clear active area (if the deleted course was active)
        while self.ui.active_course_layout.count():
            child = self.ui.active_course_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.ui.aktiv_label.setText("Current course")
        self.setup_calendar_periods()

        # Reload course list
        self.refresh_course_tiles()
        print(f"Course ID {course_id} was deleted immediately.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())