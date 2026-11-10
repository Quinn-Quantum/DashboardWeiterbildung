from dataclasses import dataclass
from Test import Test


@dataclass
class Course:
    name: str
    test: Test
    time: int

    def __init__(self, name: str, test: Test, time: int):
        self.name = name
        self.test = test
        self.time = time