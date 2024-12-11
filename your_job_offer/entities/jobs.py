from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .enums import (
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    RelocationEnum,
    EmploymentEnum,
    ScheduleEnum,
    SourceEnum,
)
from .general import *

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class VacancyModel:
    """
    Represents a job vacancy.

    Attributes:
        id (int): The unique identifier of the vacancy.
        job (Optional[str]): The job title.
        description (Optional[str]): A description of the job responsibilities.
        min_salary (Optional[int]): The minimum salary offered for the job.
        max_salary (Optional[int]): The maximum salary offered for the job.
        address (Optional[str]): The job location address.
        link (Optional[str]): A link to the job posting.
        apply_link (Optional[str]): A link where applicants can apply for the job.
        phone (Optional[str]): The contact phone number for the employer.
        email (Optional[str]): The contact email for the employer.
        employer (Optional[str]): The name of the employer or company offering the job.
        created_at (Optional[date]): The date the job vacancy was created.
        updated_at (Optional[date]): The date the job vacancy was last updated.
        work_type (Optional[WorkTypeEnum]): The type of work (e.g., full-time, part-time).
        business_trip_readiness (Optional[BusinessTripReadinessEnum]): The employer's readiness for business trips.
        work_hours (Optional[int]): The number of work hours per week.
        relocation (Optional[RelocationEnum]): Whether the employer offers relocation assistance.
        employment (Optional[EmploymentEnum]): The type of employment (e.g., contract, permanent).
        schedule (Optional[ScheduleEnum]): The preferred work schedule (e.g., flexible, 9-to-5).
        has_test (Optional[bool]): Whether there is a test associated with the job application process.
        requirement (Optional[str]): The required qualifications or skills for the job.
        responsibility (Optional[str]): The responsibilities of the role.
        area (Optional[str]): The job area or department.

    Methods:
        __str__: Returns a string representation of the VacancyModel instance.
    """

    id: Optional[int] = None
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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
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
    source: Optional[SourceEnum] = None
    id_vacancy_from_source: Optional[str] = None

    def __str__(self):
        return (
            f"Vacancy(id={self.id}, job={self.job}, description={self.description}, min_salary={self.min_salary}, "
            f"max_salary={self.max_salary}, address={self.address}, employer={self.employer}, "
            f"work_type={self.work_type}, schedule={self.schedule}, requirement={self.requirement})"
        )
