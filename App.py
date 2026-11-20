import os
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow

from calendar_helper import mark_active_course_duration, mark_study_period
from config_manager import ConfigManager
from Dashboard import Dashboard
from DatabaseConnection import DatabaseConnection
from GuiMainWindow import GuiMainWindow
from PoPUpAddCourse import PoPUpAddCourse
from PoPUpSelectDate import PoPUpSelectDate
from PoPUpSetup import PoPUpSetup
from PopUpCourseComplete import PopUpCourseComplete
from ui_helper import (
    clear_active_course_banner,
    populate_course_list,
    set_active_course_banner,
    update_course_tile_styles,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize database, dashboard, and config manager
        self.db = DatabaseConnection()
        self.config_mgr = ConfigManager("time.txt")
        self.dashboard = Dashboard(self.db, self.config_mgr)

        # Active course and dialog state
        self.active_course_id = None
        self.is_dialog_open = False

        # Initialize GUI class and apply it to the window
        self.gui = GuiMainWindow()
        self.gui.setup_ui(self)

        # Connect button click and list selection
        self.gui.add_button.clicked.connect(self.open_popup_add_course)
        self.gui.kurs_listWidget.itemClicked.connect(self.select_active_course)

        # Load config and setup calendar & courses
        self.start_date, self.total_months = self._init_config_with_setup()
        self.time_for_study = self.dashboard.lode_time()

        mark_study_period(self.gui.calendarWidget, self.start_date, self.total_months)
        self.refresh_course_tiles()

    def _init_config_with_setup(self) -> tuple[QDate, int]:
        """Opens the setup dialog on first launch if no config file exists yet."""
        if not os.path.exists(self.config_mgr.filepath):
            dialog = PoPUpSetup(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                start_str, months = dialog.get_setup_data()
                self.config_mgr.write(start_str, months)
                return QDate.fromString(start_str, "yyyy-MM-dd"), months

        return self.config_mgr.load_or_default()

    def open_popup_add_course(self):
        """Opens the add-course dialog and stores the new course in the database."""
        dialog = PoPUpAddCourse(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name_course = dialog.course_name.text()
            test_name = dialog.get_selected_test_type()
            is_mandatory = dialog.radio_one.isChecked()

            self.dashboard.store_in_db(name_course, test_name, is_mandatory)
            self.refresh_course_tiles()

    def closeEvent(self, event):
        """Closes the database connection when the main window exits."""
        self.db.close()
        event.accept()

    def refresh_course_tiles(self):
        """Loads courses from the database and restores the active course if present."""
        courses = self.dashboard.load_courses_from_db()

        active_tile, restored_id, active_start_date = populate_course_list(
            self.gui.kurs_listWidget,
            courses,
            self.delete_course_action,
        )
        self.active_course_id = restored_id

        if active_tile and active_start_date is not None:
            self.activate_course(active_tile, active_start_date)
        else:
            clear_active_course_banner(self.gui.active_course_layout, self.gui.aktiv_label)
            mark_study_period(self.gui.calendarWidget, self.start_date, self.total_months)

    def select_active_course(self, item):
        """Handles manual clicks on a course tile to activate or complete it."""
        if getattr(self, "is_dialog_open", False):
            return

        clicked_tile = self.gui.kurs_listWidget.itemWidget(item)
        if clicked_tile:
            # Skip already completed courses
            if getattr(clicked_tile, "is_complete", 0) == 1:
                print(f"Kurs '{clicked_tile.name}' ist bereits abgeschlossen und kann nicht mehr ausgewählt werden.")
                return

            try:
                self.is_dialog_open = True
                if clicked_tile.course_id == self.active_course_id:
                    self.open_popup_complete_cours(clicked_tile)
                else:
                    date_dialog = PoPUpSelectDate(self)
                    if date_dialog.exec() == QDialog.DialogCode.Accepted:
                        selected_date = date_dialog.get_selected_date()

                        # Save active course and update UI + calendar
                        self.dashboard.set_aktive_course(clicked_tile.course_id, selected_date)
                        self.activate_course(clicked_tile, selected_date)
            except Exception as e:
                print("PopUp for the start date does not work: ", e)
            finally:
                self.is_dialog_open = False

    def activate_course(self, active_tile, start_date: QDate):
        """Activates a course in the UI, updates list styles, and highlights the calendar."""
        self.active_course_id = active_tile.course_id
        update_course_tile_styles(self.gui.kurs_listWidget, self.active_course_id)
        set_active_course_banner(
            self.gui.active_course_layout,
            self.gui.aktiv_label,
            active_tile,
            start_date,
        )
        mark_active_course_duration(
            self.gui.calendarWidget,
            self.start_date,
            self.total_months,
            start_date,
        )
        print(f"Current Course loaded/activated: ID {active_tile.course_id} ({active_tile.name}) ab {start_date.toString('yyyy-MM-dd')}")
        return active_tile

    def delete_course_action(self, course_id):
        """Deletes a course from the database and refreshes the UI."""
        self.dashboard.delete_course(course_id)
        self.refresh_course_tiles()
        print(f"Course ID {course_id} was deleted immediately.")

    def edit_course_action(self, course_id:int ):
        row = self.dashboard.get_course_by_id(course_id)
        if row is None:
            return
        db_course_id, course_name, test_type_of_examination, test_is_mandatory = self.dashboard.get_cours_by_id(course_id)
        dialog = PoPUpAddCourse(
            parent=self,
            course_id=db_course_id,
            course_name=course_name,
            test_type_of_examination=test_type_of_examination,
            test_is_mandatory=test_is_mandatory,
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name_course = dialog.course_name.text().strip()
            selected_test = dialog.get_selected_test_type()
            test_value = selected_test.value if selected_test is not None else None
            is_mandatory = dialog.radio_one.isChecked()

            self.dashboard.update_in_db(db_course_id, name_course, test_value, is_mandatory)
            self.refresh_course_tiles()

    def open_popup_complete_cours(self, clicked_tile):
        """Opens the course-completion dialog and updates the database if confirmed."""
        complet_dialog = PopUpCourseComplete(self)
        if complet_dialog.exec() == QDialog.DialogCode.Accepted:
            is_complet = complet_dialog.radio_one.isChecked()
            if is_complet:
                self.dashboard.mark_course_as_complete(clicked_tile.course_id)
                self.active_course_id = None
                self.refresh_course_tiles()
                print(f"Kurs {clicked_tile.name} wurde als komplett markiert.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())