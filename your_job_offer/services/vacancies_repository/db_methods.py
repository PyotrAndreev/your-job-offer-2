from your_job_offer.services.vacancies_repository import mapper
from your_job_offer.services.vacancies_repository.db_sessions import session
from sqlalchemy import exists, select

from your_job_offer.services.vacancies_repository.jobs_db import User, Vacancy


def save_vacancy(vacancy):
    session.add(vacancy)
    session.commit()


def get_all_vacancies():
    vacancies = session.execute(select(Vacancy)).scalars().all()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.mapVacancyDbToVacancyModel(item))
    return vacanciesModels


def save_user(user):
    session.add(user)
    session.commit()


def get_user(login):
    user = session.query(User).filter_by(login=login).one()
    return user


def if_exist_user(login):
    exist = session.query(exists().where(User.login == login)).scalar()
    return exist
