from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

from sqlalchemy import Date

import db_methods
from db_methods import save_vacancy
from db_sessions import session
from enums import *

import requests

from dataclasses import dataclass

# @dataclass
# class Job:
#     job: str
#
#
# @dataclass
# class City:
#     name: str
#     areaId: str
#     areaName: str
#
#
# @dataclass
# class Vacancy:
#     id: str
#     description: str
#     min_salary: int | None
#     max_salary: int | None
#     address: str | None
#     link: str
#     apply_link: str
#     phone: str | None
#     email: str | None
#     employer: str
#     created_at: Date
#     updated_at: Date | None
#     # work_type: WorkTypeEnum
#     # buisiness_trip_readiness: BusinessTripReadinessEnum
#     # work_hours: int
#     # relocation: RelocationEnum
#     employment: EmploymentEnum
#     schedule: ScheduleEnum
#     has_test: bool
#     requirement: str
#     responsibility: str
#     job: Job
#     # country: Country
#     city: City
from jobs_db import *


def get_vacancies():
    ids = [156]
        # 156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155,
        # 96, 164, 104, 157, 107, 112, 113, 148, 114, 116, 121, 124, 125, 126]

    vacanciess = []
    for i in ids:
        vacanciess = vacanciess + get_vacancies_by_role(i)
        time.sleep(10)

    return vacanciess


def get_vacancies_by_role(role: int):
    params = {
        "professional_role": role,
        "per_page": 100,
    }

    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
    }

    res = (requests.get(f"https://api.hh.ru/vacancies", params=params, headers=headers)).json()
    if "pages" not in res:
        print("pages", res)
        return []
    pages = res["pages"]
    print(role, pages)
    vacanciess = []
    for i in range(1):
        params = {
            "professional_role": role,
            "per_page": 100,
            "page": i,
        }

        res = (requests.get(f"https://api.hh.ru/vacancies", params=params, headers=headers)).json()
        if "items" not in res:
            print(res)
            continue
        items = res["items"]
        for item in items:
            vacancy = Vacancy(
                description="",
                minSalary=item["salary"]["from"] if item["salary"] else None,
                maxSalary=item["salary"]["to"] if item["salary"] else None,
                address=item["address"]["raw"] if item["address"] else "",
                link=item["url"],
                applyLink=item["apply_alternate_url"],
                phone=None,
                email=item["contacts"]["email"] if item["contacts"] else None,
                employer=item["employer"]["name"],
                createdAt=item["created_at"],
                updatedAt=None,
                employment=EmploymentEnum(item["employment"]["id"]),
                schedule=ScheduleEnum(item["schedule"]["id"]),
                hasTest=item["has_test"],
                requirement=item["snippet"]["requirement"],
                responsibility=item["snippet"]["responsibility"],
                job=item["name"],
                area=item["area"]["name"]
            )
            save_vacancy(vacancy)
            vacanciess.append(vacancy)

    return vacanciess


get_vacancies()


