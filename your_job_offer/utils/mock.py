from os import getenv

from your_job_offer.entities.user import UserModel, VacancyModel
from your_job_offer.services.cv_parser.methods import parse
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import (
    db_methods,
    db_session,
)
import your_job_offer.models.vacancy as vacancy_models
from your_job_offer.use_cases.vacancy_cases import getAllVacancyFromDb
from your_job_offer.use_cases.user_cases import (
    ifExistUser,
    updateUser,
    saveUser,
    getUser,
)
from time import sleep


def get_all_vacancies_by_user(user: UserModel) -> list[VacancyModel]:
    vacancies = db_methods.get_vacancies_by_user(mapper.map_userModel(user))
    list_vac = []
    for item in vacancies:
        list_vac.append(mapper.map_vacancy(item))
    return list_vac


def get_all_vacancy_models() -> list[VacancyModel]:
    vacancies = db_methods.get_all_vacancies()
    return list(map(mapper.map_vacancy, vacancies))


# Предполагая, что у вас уже есть объект User и список объектов Vacancy


def apply_to_vacancies(
    user: db_methods.User, vacancies: list[db_methods.Vacancy]
):
    for vacancy in vacancies:
        # Проверяем, не связан ли пользователь с этой вакансией
        if vacancy not in user.vacancy:
            user.vacancy.append(vacancy)  # Добавляем вакансию к пользователю

    # Сохраняем изменения в сессии
    db_methods.session.add(user)
    db_methods.session.commit()


def apply_user_to_vacancies(
    user: db_methods.User, vacancies: list[db_methods.Vacancy]
):
    # Создаем связи между пользователем и каждой вакансией
    user_vacancy_links = [
        vacancy_models.UserVacancy(userId=user.id, vacancyId=vacancy.id)
        for vacancy in vacancies
    ]
    # Добавляем все связи в сессию
    db_methods.session.add_all(user_vacancy_links)
    db_methods.session.commit()


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
        sleep(5)
        for vacancy in vacancies:
            vacancy.id = None
        user.vacancy = vacancies
        saveUser(user)
        # user_model = getUser(user.login)
        # for vacancy in db_methods.get_all_vacancies():

        # user.vacancy = vacancies
        # updateUser(user)
        # sleep(2)
        # vacancies = db_methods.get_all_vacancies()
        # apply_to_vacancies(user_model, vacancies)
    return user
