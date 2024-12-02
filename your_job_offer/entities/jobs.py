from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

from .enums import WorkTypeEnum, BusinessTripReadinessEnum, RelocationEnum, EmploymentEnum, ScheduleEnum
from .general import *

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class VacancyModel:
    id: int
    job: Optional[str] = None
    description: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    address: Optional[str] = None
    link: Optional[str] = None
    apply_link: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    employer: Optional[str] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    work_type: Optional[WorkTypeEnum] = None
    business_trip_readiness: Optional[BusinessTripReadinessEnum] = None
    work_hours: Optional[int] = None
    relocation: Optional[RelocationEnum] = None
    employment: Optional[EmploymentEnum] = None
    schedule: Optional[ScheduleEnum] = None
    has_test: Optional[bool] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    area: Optional[str] = None

    def __str__(self):
        return (
            f"Vacancy(id={self.id}, job={self.job}, description={self.description}, min_salary={self.min_salary}, "
            f"max_salary={self.max_salary}, address={self.address}, employer={self.employer}, "
            f"work_type={self.work_type}, schedule={self.schedule}, requirement={self.requirement})"
        )
