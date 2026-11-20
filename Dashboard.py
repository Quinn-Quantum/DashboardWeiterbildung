from typing import Optional

from PyQt6.QtCore import QDate

from Course import Course
from DatabaseConnection import DatabaseConnection
from config_manager import ConfigManager


class Dashboard:
    def __init__(self, db: DatabaseConnection, config_mgr: Optional[ConfigManager] = None):
        self.db = db
        self.aktive_course: Optional[Course] = None
        self.config_mgr = config_mgr or ConfigManager("time.txt")

    def lode_time(self):
        """Loads study period configuration as (start_date_str, months)."""
        return self.config_mgr.load_raw()

    def store_in_db(self, name_course, test_name, is_mandatory):
        """Stores if the test is mandatory"""
        self.db.store_in_db(name_course, test_name, is_mandatory)

    def set_aktive_course(self, course_id, start_date: Optional[QDate] = None ):
        """Stores the active course in the db"""
        self.db.set_active_course_in_db(course_id, start_date)

    def load_courses_from_db(self):
        """Load all courses from the database"""
        return self.db.get_all_courses()

    def get_course_by_id(self, course_id: int):
        """Gets course by id"""
        return self.db.get_course_by_id(course_id)

    def update_in_db(self, db_course_id, name_course, test_value, is_mandatory):
        self.db.update_course_in_db(db_course_id, name_course, test_value, is_mandatory)


    def delete_course(self, course_id):
        """Forwards the delete command to the database."""
        self.db.delete_course_from_db(course_id)

    def mark_course_as_complete(self, course_id):
        """Forwards the mark command to the database."""
        self.db.mark_cours_as_complet(course_id)

    def remaining_training_days(self) -> int:
        """Calculates remaining days of the overall training period."""
        start_date, total_months = self.config_mgr.load_or_default()
        end_date = start_date.addMonths(total_months)
        return max(0, QDate.currentDate().daysTo(end_date))