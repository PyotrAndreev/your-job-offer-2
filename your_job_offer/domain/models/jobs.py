from dataclasses import dataclass

from .general import *


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
