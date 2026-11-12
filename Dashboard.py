from dataclasses import dataclass
from Course import Course
from Test import Test
import os
from DatabaseConnection import DatabaseConnection



@dataclass
class Dashboard:
    aktive_course: Course
    time: int
    cours_list: list[Course]

    def __init__(self,):
        self.cours_list = []
        self.db = DatabaseConnection()
        self.time_datei = "time.txt"

        # chaks the txt data
        self.initialisiere_time_datei()

    def initialisiere_time_datei(self):
        """Create the txt-Datei for the time i have for the study."""
        if not os.path.exists(self.time_datei):
            with open(self.time_datei, "w", encoding="utf-8") as f:
                f.write("0")  # Standardwert z.B. 0 Minuten/Stunden
            print(f"Textdatei '{self.time_datei}' wurde frisch erstellt.")

    def write_time(self, time: int):
        """write the tim in txt-Datei."""
        with open(self.time_datei, "w", encoding="utf-8") as f:
            f.write(str(time))

    def lade_time(self) -> int:
        """read the time in txt-Datei aus."""
        if os.path.exists(self.time_datei):
            with open(self.time_datei, "r", encoding="utf-8") as f:
                inhalt = f.read().strip()
                return int(inhalt) if inhalt.isdigit() else 0
        return 0

    def store_in_db(cours_list):
        pass
    def set_aktive_course(self,aktive_course: Course):
        self.aktive_course = aktive_course

    def new_course(self, name: str, test: Test,  time: int):
        new_course = Course(name, test, time)
        self.cours_list.append(new_course)
        self.store_in_db(self.cours_list)
        pass

    def load_data_from_db(self):
        pass

    def start_time(self,start:int):
        pass

    def end_time(self,end:int):
        pass


