
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
    """
    Saves a new vacancy to the database.

    Args:
        vacancy (Vacancy): The vacancy object to save.

    """
    session.add(vacancy)
    session.commit()


def get_all_vacancies() -> [Vacancy]:
    """
    Retrieves all vacancies from the database.

    Returns:
        list[Vacancy]: A list of all vacancy objects.
    """
    vacancies = session.execute(select(Vacancy)).scalars().all()
    return vacancies


def save_user(user: User)->User:
    """
    Saves a user to the database.

    Args:
        user (User): The user object to save.

    """
    session.add(user)
    session.commit()
    return user


def get_user(login: str) -> User:
    """
    Retrieves a user from the database by login and password.

    Args:
        login (str): The user's login.

    Returns:
        User: The user object associated with the provided login and password.

    Raises:
        NoResultFound: If no user is found with the provided login and password.
    """
    user = session.scalars(select(User).filter_by(login=login)).first()
    print(user)
    return user


def if_exist_user(login: str) -> bool:
    """
    Checks if a user with the given login exists in the database.

    Args:
        login (str): The user's login.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    exist = session.execute(select(User).filter_by(login=login)).scalar()
    return True if exist else False


def update_user(newUser: User):
    """
    Updates an existing user's information in the database.

    Args:
        newUser (User): The updated user object.

    Returns:
        None

    Raises:
        NoResultFound: If the user is not found.
    """
    user = get_user(newUser.login)
    user = newUser
    session.commit()


def get_vacancy(key: VacancyKey) -> Vacancy:
    """
    Retrieves a vacancy by its unique key (job ID).

    Args:
        key (VacancyKey): The key for the vacancy.

    Returns:
        Vacancy: The vacancy object associated with the provided key.

    Raises:
        NoResultFound: If no vacancy is found with the provided key.
    """
    vacancy = session.query(Vacancy).filter_by(job_id=key.id).one()
    return vacancy


def get_vacancies_with_statement(stmt):
    """
    Retrieves a list of vacancies based on a custom SQL statement.

    Args:
        stmt: The SQL statement to execute.

    Returns:
        list[Vacancy]: A list of vacancy objects returned by the query.
    """
    vacancies = []
    row = session.execute(stmt).scalars().all()
    for item in row:
        vacancies.append(item)
    return vacancies


def get_vacancies_by_employment(employment: EmploymentEnum):
    """
    Retrieves vacancies based on employment type.

    Args:
        employment (EmploymentEnum): The employment type to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified employment type.
    """
    stmt = select(Vacancy).where(Vacancy.employment == employment)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_name(job):
    """
    Retrieves vacancies based on job name.

    Args:
        job (str): The job name to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified job name.
    """
    stmt = select(Vacancy).where(Vacancy.job == job)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_schedule(schedule: ScheduleEnum):
    """
    Retrieves vacancies based on the work schedule.

    Args:
        schedule (ScheduleEnum): The work schedule to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified schedule.
    """
    stmt = select(Vacancy).where(Vacancy.schedule == schedule)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_salary(salary):
    """
    Retrieves vacancies with a minimum salary greater than or equal to the specified amount.

    Args:
        salary (int): The minimum salary to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that meet the salary condition.
    """
    stmt = select(Vacancy).where(Vacancy.minSalary >= salary)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_employer(employer):
    """
    Retrieves vacancies based on employer name.

    Args:
        employer (str): The employer name to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified employer.
    """
    stmt = select(Vacancy).where(Vacancy.employer == employer)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_work_type(work_type: WorkTypeEnum):
    """
    Retrieves vacancies based on work type.

    Args:
        work_type (WorkTypeEnum): The work type to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified work type.
    """
    stmt = select(Vacancy).where(Vacancy.workType == work_type)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_bus_trip_ready(readiness: BusinessTripReadinessEnum):
    """
    Retrieves vacancies based on business trip readiness.

    Args:
        readiness (BusinessTripReadinessEnum): The business trip readiness status to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified readiness status.
    """
    stmt = select(Vacancy).where(Vacancy.businessTripReadiness == readiness)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_test(has_test):
    """
    Retrieves vacancies based on whether a test is required.

    Args:
        has_test (bool): True if a test is required, False otherwise.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the test requirement.
    """
    stmt = select(Vacancy).where(Vacancy.hasTest == has_test)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_area(area):
    """
    Retrieves vacancies based on area/location.

    Args:
        area (str): The area to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified area.
    """
    stmt = select(Vacancy).where(Vacancy.area == area)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_relocation(relocation: RelocationEnum):
    """
    Retrieves vacancies based on relocation availability.

    Args:
        relocation (RelocationEnum): The relocation status to filter by.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the specified relocation status.
    """
    stmt = select(Vacancy).where(Vacancy.relocation == relocation)
    return get_vacancies_with_statement(stmt)


def get_vacancies_by_user(user: User):
    """
    Retrieves vacancies that match the user's preferences.

    Args:
        user (User): The user object containing preferences such as employment, work type, etc.

    Returns:
        list[Vacancy]: A list of vacancy objects that match the user's preferences.
    """
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


# def update_user(user: User):
#     """
#     Updates the information of an existing user in the database.
#
#     This function iterates over the columns of the User model (except 'id', 'login', and 'password')
#     and updates the corresponding fields of the user with the new values.
#
#     Args:
#         user (User): The updated user object.
#
#     """
#     try:
#         user = session.query(User).filter_by(login=user.login).one()
#
#         for field in User.__table__.columns.keys():
#             if field not in ['id', 'login', 'password']:
#                 new_value = getattr(user, field, None)
#                 if new_value is not None:
#                     setattr(user, field, new_value)
#         session.commit()
#         log.info(f"Пользователь с логином '{user.login}' успешно обновлен.")
#     except NoResultFound:
#         log.error(f"Пользователь с логином '{user.login}' не найден.")
#     except Exception as e:
#         log.error(f"Ошибка обновления: {e}")
#         session.rollback()
