from dataclasses import dataclass
@dataclass
class Test:
    type_of_examination: str
    is_mandatory: bool

    def __init__(self,type_of_examination: str, is_mandatory: bool):
        self.type_of_examination = type_of_examination
        self.is_mandatory = is_mandatory