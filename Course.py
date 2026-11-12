from dataclasses import dataclass
from Test import Test


@dataclass
class Course:
    name: str
    test: Test
    time: int
    is_active: bool

    def __init__(self, name: str, test: Test, time: int, is_active: bool = False) -> None:
        self.name = name
        self.test = test
        self.time = time
        self.is_active = is_active