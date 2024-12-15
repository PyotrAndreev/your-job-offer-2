from os import getenv

from your_job_offer.entities.user import UserModel, VacancyModel
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods
from your_job_offer.use_cases.vacancy_cases import getAllVacancyFromDb
from your_job_offer.use_cases.user_cases import (
    ifExistUser,
    saveUser,
)


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
    # user = parse("your_job_offer/tests/parser/files/resume1.pdf")
    user = UserModel()
    user.inner_email = getenv("EMAIL")
    user.inner_email_password = getenv("EMAIL_PASSWORD")
    user.login = "afarovruslan"
    user.password = "123"
    if not ifExistUser(user.login):
        vacancies = getAllVacancyFromDb()
        while len(vacancies) < 80:
            vacancies = getAllVacancyFromDb()
        for vacancy in vacancies:
            vacancy.id = None
        user.vacancy = vacancies
        saveUser(user)
    return user
