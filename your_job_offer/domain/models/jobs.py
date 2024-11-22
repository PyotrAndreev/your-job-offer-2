from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .general import *


class SourceEnum(Enum):
    HHRU = "hh.ru"


@dataclass
class Vacancy:
    job: Optional[str] = None
    description: Optional[str] = None
    work_type: Optional[str] = None
    min_salary: Optional[Salary] = None
    max_salary: Optional[Salary] = None
    address: Optional[str] = None
    link: Optional[str] = None
    apply_link: Optional[str] = None
    phone: Optional[Phone] = None
    email: Optional[Email] = None
    employer: Optional[str] = None
    created_at: Optional[Date] = None
    updated_at: Optional[Date] = None
    buisiness_trip_readiness: Optional[bool] = None
    work_hours: Optional[WorkHours] = None
    relocation: Optional[bool] = None
    has_test: Optional[bool] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    schedule: Optional[str] = None
    employment: Optional[str] = None
    source: SourceEnum = SourceEnum.HHRU
