


from typing import List

from .inmet import Inmet

class YearlyInmet():
    year: str
    inmet_list: List[Inmet]

    def __init__(self, year: str, inmet_list: List[Inmet]):
        self.year = year
        self.inmet_list = inmet_list