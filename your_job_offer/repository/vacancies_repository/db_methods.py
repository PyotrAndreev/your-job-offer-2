
from entities.tracking import VacancyKey
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound

import logger
from entities.enums import EmploymentEnum, ScheduleEnum, WorkTypeEnum, BusinessTripReadinessEnum, RelocationEnum
from models.user import User
from models.vacancy import Vacancy
from repository.vacancies_repository.db_session import session

log = logger.get_logger(__name__)


def save_vacancy(vacancy: Vacancy):
    session.add(vacancy)
    session.commit()


def get_all_vacancies() -> [Vacancy]:
    vacancies = session.execute(select(Vacancy)).scalars().all()
    return vacancies


def save_user(user: User):
    session.add()
    session.commit()


def get_user(login: str, password: str) -> User:
    user = session.query(User).filter_by(login=login, password=password).one()
    return user


def if_exist_user(login: str) -> bool:
    exist = session.execute(select(User).filter_by(login=login)).scalar()
    return True if exist else False


def update_user(newUser: User):
    user = get_user(newUser.login, newUser.password)
    user = newUser
    session.commit()


def get_vacancy(key: VacancyKey) -> Vacancy:
    vacancy = session.query(Vacancy).filter_by(job_id=key.id).one()
    return vacancy


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


def get_vacancies_by_user(user: User):
    stmt = select(Vacancy).where(
        or_(user.relocation is None, Vacancy.relocation == user.relocation),
        or_(user.employment is None, Vacancy.employment == user.employment),
        or_(user.workType is None, Vacancy.workType == user.workType),
        or_(user.businessTripReadiness is None, Vacancy.businessTripReadiness == user.businessTripReadiness),
        or_(user.schedule is None, Vacancy.schedule == user.schedule),
    )
    if user.workHours is not None:
        stmt = stmt.where(or_(Vacancy.workHours is None, Vacancy.workHours <= user.workHours))

    if user.minSalary is not None:
        stmt = stmt.where(or_(Vacancy.minSalary is None, Vacancy.minSalary >= user.minSalary))

    return get_vacancies_with_statement(stmt)


def update_user(user: User):
    try:
        user = session.query(User).filter_by(login=user.login).one()

        for field in User.__table__.columns.keys():
            if field not in ['id', 'login', 'password']:
                new_value = getattr(user, field, None)
                if new_value is not None:
                    setattr(user, field, new_value)
        session.commit()
        log.info(f"Пользователь с логином '{user.login}' успешно обновлен.")
    except NoResultFound:
        log.error(f"Пользователь с логином '{user.login}' не найден.")
    except Exception as e:
        log.error(f"Ошибка обновления: {e}")
        session.rollback()
