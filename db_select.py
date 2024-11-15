from db_sessions import session
from sqlalchemy import select

from jobs_db import Vacancy
from enums import EmploymentEnum, ScheduleEnum, WorkTypeEnum, BusinessTripReadinessEnum


def get_vacancies_with_statement(stmt):
    vacancies = []
    row = session.execute(stmt).scalars().all()
    for item in row:
        vacancies.append(item)
    return vacancies


def get_vacancies_by_employment(employment: EmploymentEnum):
    stmt = select(Vacancy).where(Vacancy.employment == employment)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_name(job):
    stmt = select(Vacancy).where(Vacancy.job == job)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_schedule(schedule: ScheduleEnum):
    stmt = select(Vacancy).where(Vacancy.schedule == schedule)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_salary(salary):
    stmt = select(Vacancy).where(Vacancy.minSalary >= salary)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_employer(employer):
    stmt = select(Vacancy).where(Vacancy.employer == employer)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_work_type(work_type: WorkTypeEnum):
    stmt = select(Vacancy).where(Vacancy.workType == work_type)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_bus_trip_ready(readiness: BusinessTripReadinessEnum):
    stmt = select(Vacancy).where(Vacancy.businessTripReadiness == readiness)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_test(has_test):
    stmt = select(Vacancy).where(Vacancy.hasTest == has_test)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_area(area):
    stmt = select(Vacancy).where(Vacancy.area == area)
    return get_vacancies_with_statement(stmt)
