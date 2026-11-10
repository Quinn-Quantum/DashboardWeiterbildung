from dataclasses import dataclass
from Course import Course



@dataclass
class Dashboard:
    aktive_course: Course
    time: int
    cours_list: list[Course]

    def __init__(self,aktive_course: Course):
        self.aktive_course = aktive_course
        self.time = aktive_course.time
        self.cours_list = []

    def set_aktive_course(self,aktive_course: Course):
        self.aktive_course = aktive_course

    def new_course(self):
        pass

    def load_data_from_db(self):
        pass

    def store_in_db(self):
        pass

    def start_time(self,start:int):
        pass

    def end_time(self,end:int):
        pass


