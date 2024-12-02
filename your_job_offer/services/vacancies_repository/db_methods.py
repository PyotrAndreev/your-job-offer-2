from sqlalchemy import exists, select, or_
from sqlalchemy.exc import NoResultFound

import logger
from entities.enums import EmploymentEnum, ScheduleEnum, WorkTypeEnum, BusinessTripReadinessEnum, RelocationEnum
from mappers import mapper
from models.user import User
from models.vacancy import Vacancy
from services.vacancies_repository.db_session import session

log = logger.get_logger(__name__)


def save_vacancy(vacancy: Vacancy):
    session.add(vacancy)
    session.commit()


def get_all_vacancies():
    vacancies = session.execute(select(Vacancy)).scalars().all()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.map_vacancy(item))
    return vacanciesModels


def save_user(user: User):
    session.add(user)
    session.commit()


def get_user(login: str) -> User:
    user = session.query(User).filter_by(login=login).one()
    return user


def if_exist_user(login: str) -> bool:
    exist = session.execute(select(User).filter_by(login=login)).scalar()
    return True if exist else False


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
        or_(usr.relocation is None, Vacancy.relocation == usr.relocation),
        or_(usr.employment is None, Vacancy.employment == usr.employment),
        or_(usr.workType is None, Vacancy.workType == usr.workType),
        or_(usr.businessTripReadiness is None, Vacancy.businessTripReadiness == usr.businessTripReadiness),
        or_(usr.schedule is None, Vacancy.schedule == usr.schedule),
    )
    if usr.workHours is not None:
        stmt = stmt.where(or_(Vacancy.workHours is None, Vacancy.workHours <= usr.workHours))

    if usr.minSalary is not None:
        stmt = stmt.where(or_(Vacancy.minSalary is None, Vacancy.minSalary >= usr.minSalary))

    return get_vacancies_with_statement(stmt)


def update_user(usr: User):
    try:
        user = session.query(User).filter_by(login=usr.login).one()

        for field in User.__table__.columns.keys():
            if field not in ['id', 'login', 'password']:
                new_value = getattr(usr, field, None)
                if new_value is not None:
                    setattr(user, field, new_value)
        session.commit()
        log.info(f"Пользователь с логином '{usr.login}' успешно обновлен.")
    except NoResultFound:
        log.error(f"Пользователь с логином '{usr.login}' не найден.")
    except Exception as e:
        log.error(f"Ошибка обновления: {e}")
        session.rollback()
