from dataclasses import dataclass
import re

from .general import Phone, Email, Salary, WorkHours, Date


@dataclass
class Name:
    name: str

    def __post_init__(self):
        if not re.match(
            "[A-zА-я]{2,25}", self.name
        ):  # наверное, если строка пришла какая-то не такая, то лучше
            # оставить поле пустым и пусть пользователь сам заполнит
            self.name = ""


@dataclass
class Achievement:
    title: str
    description: str
    link: str


@dataclass
class Project:
    title: str
    description: str
    link: str


@dataclass
class WorkExperience:
    job: str
    work_place: str
    description: str
    start_date: Date
    finish_date: Date


@dataclass
class User:
    birth_date: Date
    first_name: Name
    last_name: Name
    middle_name: Name
    gender: str
    phone: Phone
    email: Email
    city: str
    country: str
    cv: str
    description: str
    work_type: str
    min_salary: Salary
    max_salary: Salary
    business_trip_readiness: bool
    work_hours: WorkHours
    relocation: bool
    achievements: list[Achievement]
    projects: list[Project]
    skills: list[str]
    work_experience: list[WorkExperience]
