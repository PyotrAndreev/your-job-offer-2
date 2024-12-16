import token

from your_job_offer.entities.hh_token import HHTokenModel
from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.tracking import VacancyKey, StatusModel
from your_job_offer.entities.user import *
from your_job_offer.models.hh_token import HH_Token
from your_job_offer.models.user import (
    User,
    City,
    Country,
    Achievement,
    Project,
    WorkExperience,
    Education,
    Skill,
    Language,
)
from your_job_offer.models.vacancy import Vacancy, Status
from your_job_offer.repository.vacancies_repository.db_get_methods import get_job, get_job_id, get_professional_role


def map_user(user: User) -> UserModel:
    professional_role = get_professional_role(user.roleId) if user else None
    return UserModel(
        id=user.id,
        login=user.login,
        password=user.password,
        birth_date=user.birthDate,
        first_name=user.firstName,
        last_name=user.lastName,
        middle_name=user.middleName,
        photo=user.photo,
        gender=user.gender,
        phone=user.phone,
        email=user.email,
        city=(
            CityModel(
                id=user.city.id, name=user.city.name, area_id=user.city.areaId
            )
            if user.city
            else None
        ),
        country=(
            CountryModel(
                id=user.country.id,
                name=user.country.name,
                area_id=user.country.areaId,
            )
            if user.country
            else None
        ),
        cv=user.cv,
        description=user.description,
        work_type=user.workType,
        min_salary=user.minSalary,
        max_salary=user.maxSalary,
        business_trip_readiness=user.businessTripReadiness,
        work_hours=user.workHours,
        relocation=user.relocation,
        employment=user.employment,
        schedule=user.schedule,
        citizenship=user.citizenship,
        professional_role=(
            ProfessionalRoleModel(
                id=professional_role.id,
                role_id=user.roleId,
                name=professional_role.name,
            )
            if professional_role
            else None
        ),
        projects=[
            ProjectModel(
                id=p.id, name=p.name, description=p.description, link=p.link
            )
            for p in user.project
        ],
        achievements=[
            AchievementModel(
                id=a.id, name=a.name, description=a.description, link=a.link
            )
            for a in user.achievement
        ],
        work_experiences=[
            WorkExperienceModel(
                id=w.id,
                job=get_job(w.jobId).name if w.jobId else None,
                work_place=w.workPlace,
                description=w.description,
                start_date=w.startDate,
                finish_date=w.finishDate,
            )
            for w in user.workExperience
        ],
        educations=[
            EducationModel(
                id=e.id,
                institution=e.institution,
                major=e.major,
                degree=e.degree,
                description=e.description,
                start_date=e.startDate,
                finish_date=e.finishDate,
            )
            for e in user.education
        ],
        hh_resume_id=user.hhResumeId,
        inner_email=user.innerEmail,
        inner_email_password=user.innerEmailPassword,
        education_level=user.educationLevel,
        skills=[
            SkillModel(id=s.id, name=s.name, description=s.description)
            for s in user.skill
        ],
        languages=[
            LanguageModel(id=l.id, name=l.name, level=l.level)
            for l in user.language
        ],
        status=[map_status(s) for s in user.status],
    )


def map_vacancy(vacancy: Vacancy) -> VacancyModel:
    professional_role = (
        get_professional_role(vacancy.professionalRoleId) if vacancy else None
    )
    return VacancyModel(
        id=vacancy.id,
        job=vacancy.job,
        description=vacancy.description,
        min_salary=vacancy.minSalary,
        max_salary=vacancy.maxSalary,
        address=vacancy.address,
        link=vacancy.link,
        apply_link=vacancy.applyLink,
        phone=vacancy.phone,
        email=vacancy.email,
        employer=vacancy.employer,
        created_at=vacancy.createdAt,
        updated_at=vacancy.updatedAt,
        work_type=vacancy.workType,
        business_trip_readiness=vacancy.businessTripReadiness,
        work_hours=vacancy.workHours,
        relocation=vacancy.relocation,
        employment=vacancy.employment,
        schedule=vacancy.schedule,
        has_test=vacancy.hasTest,
        requirement=vacancy.requirement,
        responsibility=vacancy.responsibility,
        area=vacancy.area,
        source=vacancy.source,
        id_vacancy_from_source=vacancy.idVacancyFromSource,
        professional_role=(
            ProfessionalRoleModel(
                id=professional_role.id,
                role_id=vacancy.professionalRoleId,
                name=professional_role.name,
            )
            if professional_role
            else None
        ),
    )


def map_hh_token(hh_token: HH_Token) -> HHTokenModel:
    return HHTokenModel(
        id=hh_token.id,
        login=hh_token.login,
        access_token=hh_token.access_token,
        refresh_token=hh_token.refresh_token,
    )


def map_hh_token_model(hh_token: HHTokenModel) -> HH_Token:
    return HH_Token(
        id=hh_token.id,
        login=hh_token.login,
        access_token=hh_token.access_token,
        refresh_token=hh_token.refresh_token,
    )


def map_userModel(user: UserModel) -> User:
    return User(
        id=user.id,
        login=user.login,
        password=user.password,
        birthDate=user.birth_date,
        firstName=user.first_name,
        lastName=user.last_name,
        middleName=user.middle_name,
        photo=user.photo,
        gender=user.gender,
        phone=user.phone,
        email=user.email,
        city=(
            City(
                id=user.city.id, name=user.city.name, areaId=user.city.area_id
            )
            if user.city
            else None
        ),
        country=(
            Country(
                id=user.country.id,
                name=user.country.name,
                areaId=user.country.area_id,
            )
            if user.country
            else None
        ),
        cv=user.cv,
        description=user.description,
        workType=user.work_type,
        minSalary=user.min_salary,
        maxSalary=user.max_salary,
        businessTripReadiness=user.business_trip_readiness,
        workHours=user.work_hours,
        relocation=user.relocation,
        employment=user.employment,
        schedule=user.schedule,
        citizenship=user.citizenship,
        hhResumeId=user.hh_resume_id,
        innerEmail=user.inner_email,
        innerEmailPassword=user.inner_email_password,
        roleId=(
            user.professional_role.role_id
            if user and user.professional_role
            else None
        ),
        project=[
            Project(
                id=p.id, name=p.name, description=p.description, link=p.link
            )
            for p in user.projects
        ],
        achievement=[
            Achievement(
                id=a.id, name=a.name, description=a.description, link=a.link
            )
            for a in user.achievements
        ],
        workExperience=[
            WorkExperience(
                id=w.id,
                jobId=get_job_id(w.job) if w.job else None,
                workPlace=w.work_place,
                description=w.description,
                startDate=w.start_date,
                finishDate=w.finish_date,
            )
            for w in user.work_experiences
        ],
        education=[
            Education(
                id=e.id,
                institution=e.institution,
                major=e.major,
                degree=e.degree,
                description=e.description,
                startDate=e.start_date,
                finishDate=e.finish_date,
            )
            for e in user.educations
        ],
        educationLevel=user.education_level,
        skill=[
            Skill(id=s.id, name=s.name, description=s.description)
            for s in user.skills
        ],
        language=[Language(id=l.id, name=l.name) for l in user.languages],
        vacancy=[map_status_model(s) for s in user.status],
    )


def map_vacancy_model(vacancy: VacancyModel) -> Vacancy:
    return Vacancy(
        id=vacancy.id,
        job=vacancy.job,
        description=vacancy.description,
        minSalary=vacancy.min_salary,
        maxSalary=vacancy.max_salary,
        address=vacancy.address,
        link=vacancy.link,
        applyLink=vacancy.apply_link,
        phone=vacancy.phone,
        email=vacancy.email,
        employer=vacancy.employer,
        createdAt=vacancy.created_at,
        updatedAt=vacancy.updated_at,
        workType=vacancy.work_type,
        businessTripReadiness=vacancy.business_trip_readiness,
        workHours=vacancy.work_hours,
        relocation=vacancy.relocation,
        employment=vacancy.employment,
        schedule=vacancy.schedule,
        hasTest=vacancy.has_test,
        requirement=vacancy.requirement,
        responsibility=vacancy.responsibility,
        area=vacancy.area,
        source=vacancy.source,
        idVacancyFromSource=vacancy.id_vacancy_from_source,
        professionalRoleId=(
            vacancy.professional_role.role_id
            if vacancy and vacancy.professional_role
            else None
        ),
        status=[map_status_model(status) for status in vacancy.status],
    )


def map_vacancy_db_to_vacancy_key(vacancy_db: Vacancy) -> VacancyKey:
    return VacancyKey(
        job=vacancy_db.job,
        employer=vacancy_db.employer,
        id_vacancy_from_source=vacancy_db.idVacancyFromSource,
    )


def map_status_model(status: StatusModel) -> Status:
    return Status(
        id=status.id,
        statusField=status.status,
        deadline=status.deadline,
        date=status.date,
        message=status.message,
        vacancy=map_vacancy_model(status.vacancy)
    )


def map_status(status: Status) -> StatusModel:
    return StatusModel(
        id=status.id,
        status=status.statusField,
        deadline=status.deadline,
        date=status.date,
        message=status.message,
        vacancy=map_vacancy(status.vacancy)
    )
