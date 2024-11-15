import jobs_db
from enums import BusinessTripReadinessEnum, RelocationEnum
from models import Vacancy, Salary, Phone, Email, Date, WorkHours
import pandas as pd


def mapVacancyDbToVacancyModel(vacancyDb: jobs_db.Vacancy):
    return Vacancy(job=vacancyDb.job,
                   description=vacancyDb.description,
                   work_type=vacancyDb.workType,
                   min_salary=Salary(salary=vacancyDb.minSalary),
                   max_salary=Salary(salary=vacancyDb.maxSalary),
                   address=vacancyDb.address,
                   link=vacancyDb.link,
                   apply_link=vacancyDb.applyLink,
                   phone=Phone(phohe=vacancyDb.phone),
                   email=Email(email=vacancyDb.email),
                   employer=vacancyDb.employer,
                   created_at=Date(vacancyDb.createdAt),
                   updated_at=Date(vacancyDb.updatedAt),
                   buisiness_trip_readiness=vacancyDb.businessTripReadiness == BusinessTripReadinessEnum.READY,
                   work_hours=WorkHours(hours=vacancyDb.workHours),
                   relocation=vacancyDb.relocation != RelocationEnum.NO,
                   has_test=vacancyDb.hasTest,
                   responsibility=vacancyDb.responsibility,
                   requirement=vacancyDb.requirement,
                   schedule=str(vacancyDb.schedule),
                   employment=str(vacancyDb.employment),
                   )
