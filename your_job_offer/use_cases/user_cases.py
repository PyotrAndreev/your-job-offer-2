from typing import Optional

from your_job_offer.entities.user import UserModel
from your_job_offer.entities.tracking import VacancyKey
from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.repository.vacancies_repository import db_methods
from your_job_offer.mappers import mapper

from your_job_offer.use_cases.emails import emails, passwords

index = 0


def getUser(login: str) -> UserModel:
    user = db_methods.get_user(login=login)
    return mapper.map_user(user)


def saveUser(user: UserModel) -> UserModel:
    global index
    user.innerEmail = emails[index] if index < 20 else None
    user.innerEmailPassword = passwords[index] if index < 20 else None
    user = db_methods.save_user(mapper.map_userModel(user))
    index += 1
    return mapper.map_user(user)


def updateUser(user: UserModel) -> UserModel:
    return db_methods.update_user(user)


def ifExistUser(login: str) -> bool:
    return db_methods.if_exist_user(login=login)


def get_all_users() -> list[UserModel]:
    user_models = []
    for user in db_methods.get_all_users():
        user_models.append(mapper.map_user(user))
    return user_models


def get_all_statuses_messages(user: UserModel) -> list[str]:
    ans: list[str] = []
    for vacancy in user.vacancy:
        for status in vacancy.status:
            ans.append(status.message)
    return ans


def get_vacancies_by_keys(
        keys: list[VacancyKey], user: UserModel
) -> list[Optional[VacancyModel]]:
    vacancies = []
    userVacancies = user.vacancy
    for key in keys:
        appropriate_vacancies = []
        if key.id_vacancy_from_source is not None:
            appropriate_vacancies = [
                vacancy
                for vacancy in userVacancies
                if vacancy.id_vacancy_from_source == key.id_vacancy_from_source
            ]
        else:
            appropriate_vacancies = [
                vacancy
                for vacancy in userVacancies
                if vacancy.job == key.job and vacancy.employer == key.employer
            ]
        if len(appropriate_vacancies) > 0:
            vacancies.append(appropriate_vacancies[0])
        else:
            vacancies.append(None)
    return vacancies

