from typing import List, Optional
from Course import Course
from DatabaseConnection import DatabaseConnection
import os


class Dashboard:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.course_list: List[Course] = []
        self.aktive_course: Optional[Course] = None
        self.period_datei = "time.txt"

        self.initialisiere_period_datei()

    def initialisiere_period_datei(self):
        if not os.path.exists(self.period_datei):
            with open(self.period_datei, "w", encoding="utf-8") as f:
                f.write("Gesamtzeitraum: 6 Monate (Start: 19.10.)")

    def lade_time(self) -> str:
        if os.path.exists(self.period_datei):
            with open(self.period_datei, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "6 Monate"

    def store_in_db(self, name_course, test_name, is_mandatory):
        self.db.store_in_db(name_course, test_name, is_mandatory)

    def set_aktive_course(self, course_id, start_date_str ):
        """Speichert den aktiven Kurs in der Datenbank"""
        self.db.set_active_course_in_db(course_id, start_date_str)

    def load_courses_from_db(self):
        return self.db.get_all_courses()