from your_job_offer.entities.tracking import VacancyKey
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound

import your_job_offer.logger as logger
from your_job_offer.entities.user import UserModel
from your_job_offer.entities.enums import (
    EmploymentEnum,
    ScheduleEnum,
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    RelocationEnum,
)
from your_job_offer.models.user import (
    User,
    Job,
    City,
    Country,
    Project,
    Achievement,
    Skill,
    WorkExperience,
    Language,
    Education,
    ProfessionalRole,
)
from your_job_offer.models.vacancy import Vacancy, Status
from your_job_offer.repository.vacancies_repository.db_session import session
from your_job_offer.entities.tracking import VacancyKey
from your_job_offer.mappers.mapper import map_vacancy_model

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


def save_role(role: ProfessionalRole):
    session.add(role)
    session.commit()


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
        or_(user.relocation == None, Vacancy.relocation == user.relocation, Vacancy.relocation == None),
        or_(user.employment == None, Vacancy.employment == user.employment, Vacancy.employment == None),
        or_(user.workType == None, Vacancy.workType == user.workType, Vacancy.workType == None),
        or_(
            user.businessTripReadiness == None,
            Vacancy.businessTripReadiness == user.businessTripReadiness,
            Vacancy.businessTripReadiness == None
        ),
        or_(user.schedule == None, Vacancy.schedule == user.schedule, Vacancy.schedule == None),
        or_(user.roleId == None, Vacancy.professionalRoleId == user.roleId, Vacancy.professionalRoleId == None),
        Vacancy.hasTest == False
    )
    if user.workHours != None:
        stmt = stmt.where(
            or_(Vacancy.workHours == None, Vacancy.workHours <= user.workHours)
        )

    if user.minSalary != None:
        stmt = stmt.where(
            or_(Vacancy.minSalary == None, Vacancy.minSalary >= user.minSalary)
        )

    return get_vacancies_with_statement(stmt)


def save_job(job: Job):
    session.add(job)
    session.commit()


def if_exist_job_by_name(name: str) -> bool:
    exist = session.execute(select(Job).filter_by(name=name)).scalar()
    return True if exist else False


def get_job_by_name(name: str) -> int:
    job = session.scalars(select(Job).filter_by(name=name)).first()
    return job


def get_job_id(name: str) -> int:
    job = session.scalars(select(Job).filter_by(name=name)).first()
    return job.id


def update_user(updated_user: UserModel):
    try:
        user = get_user(updated_user.login)
        stat = list()
        if updated_user.status != None:
            for s in updated_user.status:
                st = session.scalars(select(Status).filter_by(id=s.id)).first()
                stat.append(st)
        if user.status:
            for s in user.status:
                stat.append(s)

        if updated_user.city:
            if not if_exist_city(updated_user.city.name):
                save_city(
                    City(
                        name=updated_user.city.name,
                        areaId=updated_user.city.area_id,
                    )
                )
            city = session.scalars(
                select(City).filter_by(name=updated_user.city.name)
            ).first()
            user.cityId = city.id

        if updated_user.country:
            if not if_exist_city(updated_user.country.name):
                save_country(
                    Country(
                        name=updated_user.country.name,
                        areaId=updated_user.country.area_id,
                    )
                )
            country = session.scalars(
                select(Country).filter_by(name=updated_user.country.name)
            ).first()
            user.countryId = country.id

        if updated_user.professional_role:
            user.roleId = updated_user.professional_role.role_id

        user.birthDate = updated_user.birth_date if updated_user.birth_date else user.birthDate
        user.firstName = updated_user.first_name
        user.lastName = updated_user.last_name
        user.middleName = updated_user.middle_name if updated_user.middle_name else user.middleName
        user.photo = updated_user.photo
        user.gender = updated_user.gender if updated_user.gender else user.gender
        user.phone = updated_user.phone
        user.email = updated_user.email if updated_user.email else user.email
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
        user.hhResumeId = updated_user.hh_resume_id if updated_user.hh_resume_id != None else user.hhResumeId
        user.innerEmail = updated_user.inner_email if updated_user.inner_email else user.innerEmail
        user.innerEmailPassword = updated_user.inner_email_password if updated_user.inner_email_password else user.innerEmailPassword
        user.project = (
            list(
                Project(name=p.name, description=p.description, link=p.link)
                for p in updated_user.projects
            )
            if updated_user.projects
            else user.project
        )
        user.achievement = (
            list(
                Achievement(
                    name=a.name, description=a.description, link=a.link
                )
                for a in updated_user.achievements
            )
            if updated_user.achievements
            else user.achievement
        )

        jobs = list()
        for w in updated_user.work_experiences:
            if if_exist_job_by_name(w.job):
                job = get_job_by_name(w.job)
                jobs.append(job)
            else:
                job = Job(name=w.job)
                save_job(job)
                job = get_job_by_name(w.job)
                jobs.append(job)

        user.workExperience = (
            list(
                WorkExperience(jobId=get_job_id(w.job), userId=user.id, workPlace=w.work_place, startDate=w.start_date,
                               finishDate=w.finish_date, description=w.description)
                for w in updated_user.work_experiences
            )
            if updated_user.work_experiences
            else user.workExperience
        )

        user.education = (
            list(
                Education(
                    description=e.description,
                    institution=e.institution,
                    finishDate=e.finish_date,
                )
                for e in updated_user.educations
            )
            if updated_user.educations
            else user.education
        )
        user.skill = (
            list(
                Skill(name=s.name, description=s.description)
                for s in updated_user.skills
            )
            if updated_user.skills
            else user.skill
        )
        user.language = (
            list(
                Language(name=lan.name, level=lan.level)
                for lan in updated_user.languages
            )
            if updated_user.languages
            else user.language
        )
        user.status = stat
        session.commit()
    except Exception as e:
        log.error(f"Error: {e}", exc_info=True)


def get_all_users() -> list[User]:
    users = session.execute(select(User)).scalars().all()
    return users


def get_vacancy_by_id(vacancy_id: int) -> Vacancy:
    return session.get(Vacancy, vacancy_id)


def update_statuses(vacancy_ids: list[int], statuses: list[Status]):
    for vacancy_id, status in zip(vacancy_ids, statuses):
        vacancy = get_vacancy_by_id(vacancy_id)
        if (
                session.query(Status)
                        .filter_by(message=status.message)
                        .one_or_none()
                is None
        ):
            vacancy.status.append(status)
    session.commit()


def update_status(login, vacancy_id, status):
    vacancy_bd = session.scalars(select(Vacancy).filter_by(id=vacancy_id)).first()
    user_bd = session.scalars(select(User).filter_by(login=login)).first()
    statuses = list()
    if user_bd.status != None:
        for s in user_bd.status:
            s = session.scalars(select(Status).filter_by(id=s.id)).first()
            statuses.append(s)
    statuses.append(Status(statusField=status, vacancy=vacancy_bd))
    user_bd.status = statuses
    session.commit()
