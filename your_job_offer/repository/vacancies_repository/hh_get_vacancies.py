from __future__ import annotations
import time

import requests

from your_job_offer.logger import get_logger
from your_job_offer.entities.enums import EmploymentEnum, ScheduleEnum
from your_job_offer.models.vacancy import Vacancy

log = get_logger("jobs_db_parsing")


def get_vacancies():
    ids = [
        156,
        # 160,
        # 10,
        # 12,
        # 150,
        # 25,
        # 165,
        # 34,
        # 36,
        # 73,
        # 155,
        # 96,
        # 164,
        # 104,
        # 157,
        # 107,
        # 112,
        # 113,
        # 148,
        # 114,
        # 116,
        # 121,
        # 124,
        # 125,
        # 126,
    ]

    vacanciess = []
    for i in ids:
        vacanciess = vacanciess + get_vacancies_by_role(i)
        time.sleep(5)

    return vacanciess


def get_vacancies_by_role(role: int):
    params = {
        "professional_role": role,
        "per_page": 100,
    }

    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
    }

    res = (
        requests.get(
            "https://api.hh.ru/vacancies", params=params, headers=headers
        )
    ).json()
    if "pages" not in res:
        log.info(f"pages not in {res}")
        return []
    # pages = res["pages"]
    pages = 1
    log.info(f"role={role}, pages={pages}")
    vacanciess = []
    for i in range(pages):
        params = {
            "professional_role": role,
            "per_page": 100,
            "page": i,
        }

        res = (
            requests.get(
                "https://api.hh.ru/vacancies", params=params, headers=headers
            )
        ).json()
        if "items" not in res:
            log.info(f"item not in {res}")
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
                createdAt=None,
                updatedAt=None,
                employment=EmploymentEnum(item["employment"]["id"]),
                schedule=ScheduleEnum(item["schedule"]["id"]),
                hasTest=item["has_test"],
                requirement=item["snippet"]["requirement"],
                responsibility=item["snippet"]["responsibility"],
                job=item["name"],
                area=item["area"]["name"],
            )
            vacanciess.append(vacancy)

    return vacanciess
