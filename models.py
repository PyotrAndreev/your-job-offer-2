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

    # def __post_init__(self):
    #     if not re.match("^\\+?[1-9][0-9]{7,14}$", self.phohe):
    #         self.phohe = ""


@dataclass
class Email:
    email: str

    # def __post_init__(self):
    #     if not re.match(r"^\S+@\S+\.\S+$", self.email):
    #         self.email = ""


@dataclass
class Salary:
    salary: int

    # def __post_init__(self):
    #     if isinstance(self.salary, str):
    #         if len(self.salary) == 0:
    #             self.salary = 0
    #         else:
    #             self.salary = int(self.salary)
    #     self.salary = max(0, self.salary)


@dataclass
class WorkHours:  # TODO добавить range типа 20-40
    hours: int


@dataclass
class Vacancy:
    job: str
    description: str
    work_type: str
    min_salary: Salary
    max_salary: Salary
    address: str
    link: str
    apply_link: str
    phone: Phone
    email: Email
    employer: str
    created_at: Date
    updated_at: Date
    buisiness_trip_readiness: bool
    work_hours: WorkHours
    relocation: bool
    has_test: bool
    requirement: str
    responsibility: str
    schedule: str
    employment: str
