import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QTextCharFormat, QColor

from CourseTile import CourseTile
from Dashboard import Dashboard
from DatabaseConnection import DatabaseConnection
from GuiMainWindow import GuiMainWindow
from PoPUpAddCourse import PoPUpAddCourse
from PoPUpSelectDate import PoPUpSelectDate
from PoPUpSetup import PoPUpSetup

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Database and Dashboard
        self.db = DatabaseConnection()
        self.dashboard = Dashboard(self.db)


        # Initialize GUI class and apply it to the window
        self.gui = GuiMainWindow()
        self.gui.setup_ui(self)

        # Connect button click and list selection
        self.gui.add_button.clicked.connect(self.open_popup_add_course) # Submission of the reference for later
        #Course aktiv
        self.gui.kurs_listWidget.itemClicked.connect(self.select_active_course)

        #config
        self.config_file = "time.txt"
        self.start_date, self.total_months = self.load_or_create_config()

        # Setup calendar & load courses
        self.time_for_study = self.dashboard.lade_time()
        self.setup_calendar_periods()
        self.refresh_course_tiles()

    def write_in_time(self,start_str,months):
        with open(self.config_file, "w", encoding="utf-8") as f:
            f.write(f"{start_str}\n{months}")

    def load_or_create_config(self):
        """Checks if time.txt exists. If not, the setup dialog opens."""
        if not os.path.exists(self.config_file):
            # Setup-Dialog call
            dialog = PoPUpSetup(None)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                start_str, months = dialog.get_setup_data()
                # In time.txt save
                self.write_in_time(start_str, months)
                return QDate.fromString(start_str, "yyyy-MM-dd"), months
            else:
                # when aborting uses standard values
                print("Enter default values")
                default_date = QDate.currentDate()
                default_months = 6
                start_str = default_date.toString("yyyy-MM-dd")
                self.write_in_time(start_str, default_months)
                return default_date, default_months
        else:
            # read time.txt
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    start_date = QDate.fromString(lines[0], "yyyy-MM-dd")
                    months = int(lines[1])
                    return start_date, months
            except Exception as e:
                print(f"Error by time.txt: {e}")
                print("Enter default values")
                default_date = QDate.currentDate()
                default_months = 6
                start_str = default_date.toString("yyyy-MM-dd")
                self.write_in_time(start_str, default_months)
                return QDate.currentDate(), 6

    def open_popup_add_course(self):
        dialog = PoPUpAddCourse(self)
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
        self.gui.kurs_listWidget.clear()
        courses = self.dashboard.load_courses_from_db()

        active_tile_to_restore = None
        active_start_date = None

        for course_data in courses:
            c_id, name, time, test_name, is_mandatory, is_active, start_date = course_data
            tile = CourseTile(c_id, name, test_name, is_mandatory)

            tile.delete_requested.connect(self.delete_course_action)

            item = QListWidgetItem(self.gui.kurs_listWidget)
            item.setSizeHint(tile.sizeHint())
            self.gui.kurs_listWidget.setItemWidget(item, tile)

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
        clicked_tile = self.gui.kurs_listWidget.itemWidget(item)
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
        for i in range(self.gui.kurs_listWidget.count()):
            it = self.gui.kurs_listWidget.item(i)
            tile = self.gui.kurs_listWidget.itemWidget(it)

            if tile.course_id == active_tile.course_id:
                tile.set_active_style(True)

                # Remove old active entry at the top
                while self.gui.active_course_layout.count():
                    child = self.gui.active_course_layout.takeAt(0)
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

                self.gui.active_course_layout.addWidget(active_display_tile)
                active_display_tile.show()

                self.gui.aktiv_label.setText(f"Current Course: {tile.name} (Start: {start_date.toString('dd.MM.yyyy')})")
                print(f"Current Course loaded/activated: ID {tile.course_id} ({tile.name}) ab {start_date.toString('yyyy-MM-dd')}")

                self.highlight_course_duration(start_date)
            else:
                tile.set_active_style(False)

    def setup_calendar_periods(self):

        current_year = QDate.currentDate().year()
        start_date = self.start_date
        end_date = start_date.addMonths(self.total_months)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#e2e8f0"))

        d = start_date
        while d <= end_date:
            self.gui.calendarWidget.setDateTextFormat(d, fmt)
            d = d.addDays(1)

    def highlight_course_duration(self, start_date: QDate):
        self.setup_calendar_periods()
        end_date = start_date.addDays(28)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#6e35c9"))
        fmt.setForeground(QColor("white"))

        d = start_date
        while d <= end_date:
            self.gui.calendarWidget.setDateTextFormat(d, fmt)
            d = d.addDays(1)

    def delete_course_action(self, course_id):
        """Called when the X in a tile is clicked."""
        # Delete from DB
        self.dashboard.delete_course(course_id)

        # Clear active area (if the deleted course was active)
        while self.gui.active_course_layout.count():
            child = self.gui.active_course_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.gui.aktiv_label.setText("Current course")
        self.setup_calendar_periods()

        # Reload course list
        self.refresh_course_tiles()
        print(f"Course ID {course_id} was deleted immediately.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())