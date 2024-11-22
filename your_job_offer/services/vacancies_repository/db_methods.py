from sqlalchemy import exists, select

from your_job_offer.domain.models.tracking import VacancyKey, Vacancy

from your_job_offer.services.vacancies_repository import mapper
from your_job_offer.services.vacancies_repository.db_sessions import session
from your_job_offer.services.vacancies_repository.jobs_db import (
    User as DBUser,
    Vacancy as DBVacancy,
)


def save_vacancy(vacancy):
    session.add(vacancy)
    session.commit()


def get_all_vacancies():
    vacancies = session.execute(select(DBVacancy)).scalars().all()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.mapVacancyDbToVacancyModel(item))
    return vacanciesModels


def save_user(user):
    session.add(user)
    session.commit()


def get_user(login):
    user = session.query(DBUser).filter_by(login=login).one()
    return user


def if_exist_user(login):
    exist = session.query(exists().where(DBUser.login == login)).scalar()
    return exist


def get_vacancy(key: VacancyKey) -> Vacancy:  # TODO Даша и Настя
    return Vacancy(job=key.id)
