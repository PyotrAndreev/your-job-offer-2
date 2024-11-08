from dataclasses import dataclass
import re

import pandas as pd


class Date(pd.Timestamp):
    def __init__(self, date: str):
        try:
            pd.Timestamp(date)
            super().__init__(date)
        except Exception:
            super().__init__()


@dataclass
class Phone:
    phohe: str

    def __post_init__(self):
        if not re.match("^\\+?[1-9][0-9]{7,14}$", self.phohe):
            self.phohe = ""


@dataclass
class Email:
    email: str

    def __post_init__(self):
        if not re.match(r"^\S+@\S+\.\S+$", self.email):
            self.email = ""


@dataclass
class Salary:
    salary: int | str

    def __post_init__(self):
        if isinstance(self.salary, str):
            if len(self.salary) == 0:
                self.salary = 0
            else:
                self.salary = int(self.salary)
        self.salary = max(0, self.salary)


@dataclass
class WorkHours:  # TODO добавить range типа 20-40
    hours: int
