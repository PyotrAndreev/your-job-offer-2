from os import getenv

from your_job_offer.entities.user import *
from your_job_offer.services.cv_parser.methods import parse
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods


def get_all_vacancies_by_user(user: UserModel) -> list[VacancyModel]:
    vacancies = db_methods.get_vacancies_by_user(mapper.map_userModel(user))
    list_vac = []
    for item in vacancies:
        list_vac.append(mapper.map_vacancy(item))
    return list_vac


def get_all_vacancy_models() -> list[VacancyModel]:
    vacancies = db_methods.get_all_vacancies()
    return list(map(mapper.map_vacancy, vacancies))


def get_user() -> UserModel:
    user = parse("your_job_offer/tests/parser/files/resume1.pdf")
    user.inner_email = getenv("EMAIL")
    user.inner_email_password = getenv("EMAIL_PASSWORD")
    user.vacancy = get_all_vacancy_models()
    user.login = "afarovruslan"
    return user
