from typing import Optional
from Course import Course
from DatabaseConnection import DatabaseConnection
from datetime import date
import os


class Dashboard:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.aktive_course: Optional[Course] = None
        self.period_datei = "time.txt"

    def lade_time(self):
        """Reads the start date and total duration from the time.txt."""
        if os.path.exists(self.period_datei):
            try:
                with open(self.period_datei, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    if len(lines) >= 2:
                        start_date = lines[0]  # Z.B. "2026-10-19"
                        months = int(lines[1])  # Z.B. 6
                        return start_date, months
            except Exception as e:
                print(f"Error reading the time.txt: {e}")

        # Fallback values if the file does not already exist
        today_str = date.today().strftime("%Y-%m-%d")
        return today_str, 6

    def store_in_db(self, name_course, test_name, is_mandatory):
        """Stores if the test is mandatory"""
        self.db.store_in_db(name_course, test_name, is_mandatory)

    def set_aktive_course(self, course_id, start_date_str ):
        """Stores the active course in the db"""
        self.db.set_active_course_in_db(course_id, start_date_str)

    def load_courses_from_db(self):
        """Load all courses from the database"""
        return self.db.get_all_courses()

    def delete_course(self, course_id):
        """Forwards the delete command to the database."""
        self.db.delete_course_from_db(course_id)

    def mark_cours_as_complet(self,course_id):
        self.db.mark_cours_as_complet(course_id)