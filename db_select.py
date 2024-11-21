from db_sessions import session
from sqlalchemy import select, or_, and_

from jobs_db import Vacancy, User
from enums import EmploymentEnum, ScheduleEnum, WorkTypeEnum, BusinessTripReadinessEnum, RelocationEnum


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


def get_vacancies_by_relocation(relocation: RelocationEnum):
    stmt = select(Vacancy).where(Vacancy.relocation == relocation)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_user(usr: User):
    stmt = select(Vacancy).where(
        or_(usr.relocation == None, Vacancy.relocation == usr.relocation),
        or_(usr.employment == None, Vacancy.employment == usr.employment),
        or_(usr.workType == None, Vacancy.workType == usr.workType),
        or_( usr.businessTripReadiness == None, Vacancy.businessTripReadiness == usr.businessTripReadiness),
        or_(usr.schedule == None, Vacancy.schedule == usr.schedule),
    )
    if usr.workHours != None:
        stmt = stmt.where(or_(Vacancy.workHours == None, Vacancy.workHours <= usr.workHours))

    if usr.minSalary != None:
        stmt = stmt.where(or_(Vacancy.minSalary == None, Vacancy.minSalary >= usr.minSalary))

    return get_vacancies_with_statement(stmt)


# user = User(firstName="Daria", minSalary=100000)
# vac = get_vacancies_by_user(user)
# for i in vac:
#     print(i.job, ' ', i.minSalary)
