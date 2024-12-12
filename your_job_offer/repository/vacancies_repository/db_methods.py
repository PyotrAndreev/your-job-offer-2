from typing import Optional

from entities.tracking import VacancyKey
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound

import logger as logger
from entities.enums import (
    EmploymentEnum,
    ScheduleEnum,
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    RelocationEnum,
)
from models.user import User, Job, City, Country, Project, Achievement, Skill, WorkExperience, Language, Education
from models.vacancy import Vacancy
from repository.vacancies_repository.db_session import session
from entities.tracking import VacancyKey, VacancyModel

from entities.user import UserModel

log = logger.get_logger(__name__)


def save_vacancy(vacancy: Vacancy):
    """
    Saves a new vacancy to the database.

    Args:
        vacancy (Vacancy): The vacancy object to save.

    """
    session.add(vacancy)
    session.commit()


def save_country(country: Country):
    session.add(country)
    session.commit()


def if_exist_city(name: str) -> bool:
    exist = session.execute(select(City).filter_by(name=name)).scalar()
    return True if exist else False


def if_exist_country(name: str) -> bool:
    exist = session.execute(select(Country).filter_by(name=name)).scalar()
    return True if exist else False


def save_city(city: City):
    session.add(city)
    session.commit()


def get_all_vacancies() -> list[Vacancy]:
    """
    Retrieves all vacancies from the database.

    Returns:
        list[Vacancy]: A list of all vacancy objects.
    """
    vacancies = session.execute(select(Vacancy)).scalars().all()
    return vacancies


def save_user(user: User) -> User:
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
    return user


def get_job(job_id: int) -> Job:
    job = session.scalars(select(Job).filter_by(id=job_id)).first()
    return job


def get_job_id(name: str) -> int:
    job = session.scalars(select(Job).filter_by(name=name)).first()
    return job


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
    vacancy = session.scalars(select(Vacancy).filter_by(job_id=key.id)).first()
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


def get_vacancies_by_filters(filters: dict):
    query = session.query(Vacancy)
    for key, value in filters.items():
        if value is not None:
            query = query.filter(
                getattr(Vacancy, key) == value
            )  # Простое сравнение для числовых значений

    vacancies = query.all()
    print(vacancies)


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
        or_(
            user.businessTripReadiness is None,
            Vacancy.businessTripReadiness == user.businessTripReadiness,
        ),
        or_(user.schedule is None, Vacancy.schedule == user.schedule),
    )
    if user.workHours is not None:
        stmt = stmt.where(
            or_(Vacancy.workHours is None, Vacancy.workHours <= user.workHours)
        )

    if user.minSalary is not None:
        stmt = stmt.where(
            or_(Vacancy.minSalary is None, Vacancy.minSalary >= user.minSalary)
        )

    return get_vacancies_with_statement(stmt)


def update_user(updated_user: UserModel):
    try:
        user = get_user(updated_user.login)
        if updated_user.city:
            if not if_exist_city(updated_user.city.name):
                save_city(City(name=updated_user.city.name, areaId=updated_user.city.area_id))
            city = session.scalars(select(City).filter_by(name=updated_user.city.name)).first()
            user.cityId = city.id

        if updated_user.country:
            if not if_exist_city(updated_user.country.name):
                save_country(Country(name=updated_user.country.name, areaId=updated_user.country.area_id))
            country = session.scalars(select(Country).filter_by(name=updated_user.country.name)).first()
            user.countryId = country.id

        user.birthDate = updated_user.birth_date
        user.firstName = updated_user.first_name
        user.lastName = updated_user.last_name
        user.middleName = updated_user.middle_name
        user.photo = updated_user.photo
        user.gender = updated_user.gender
        user.phone = updated_user.phone
        user.email = updated_user.email
        # user.city = City(name=updated_user.city.name,
        #                  areaId=updated_user.city.area_id) if updated_user.city else None
        # user.country = Country(name=updated_user.country.name,
        #                        areaId=updated_user.country.area_id) if updated_user.country else None,
        user.cv = updated_user.cv
        user.description = updated_user.description
        user.workType = updated_user.work_type
        user.minSalary = updated_user.min_salary
        user.maxSalary = updated_user.max_salary
        user.businessTripReadiness = updated_user.business_trip_readiness
        user.workHours = updated_user.work_hours
        user.relocation = updated_user.relocation
        user.employment = updated_user.employment
        user.schedule = updated_user.schedule
        user.citizenship = updated_user.citizenship
        user.educationLevel = updated_user.education_level
        user.hhResumeId = updated_user.hh_resume_id
        user.innerEmail = updated_user.inner_email
        user.innerEmailPassword = updated_user.inner_email_password
        user.project = list(Project(name=p.name, description=p.description, link=p.link) for p in
                            updated_user.projects) if updated_user.projects else user.project
        user.achievement = list(Achievement(name=a.name, description=a.description, link=a.link) for a in
                                updated_user.achievements) if updated_user.achievements else user.achievement
        user.workExperience = list(WorkExperience(description=w.description) for w in
                                   updated_user.work_experiences) if updated_user.work_experiences else user.workExperience
        user.education = list(
            Education(description=e.description) for e in
            updated_user.educations) if updated_user.educations else user.education
        user.skill = list(
            Skill(name=s.name, description=s.description) for s in
            updated_user.skills) if updated_user.skills else user.skill
        user.language = list(
            Language(name=lan.name) for lan in updated_user.languages) if updated_user.languages else user.language
        user.vacancy = list(
            Vacancy(description=v.description) for v in updated_user.vacancy) if updated_user.vacancy else user.vacancy
        session.commit()
    except Exception as e:
        log.error(f"Error: {e}", exc_info=True)


def get_vacancies_by_keys(
        keys: list[VacancyKey], user: UserModel,
) -> list[Optional[VacancyModel]]:
    vacancies = []
    userVacancies = user.vacancy
    print(userVacancies)
    for key in keys:
        l = []
        if key.id_vacancy_from_source is not None:
            l = [x for x in userVacancies if x.id_vacancy_from_source == key.id_vacancy_from_source]

        else:
            l = [x for x in userVacancies if x.job == key.job and x.employer == key.employer]
        if len(l) > 0:
            vacancies.append(l[0])
        else:
            vacancies.append(None)

    return vacancies
