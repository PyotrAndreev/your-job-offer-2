from entities.jobs import VacancyModel
from entities.user import *
from models.user import User
from models.vacancy import Vacancy


def map_user(user: User) -> UserModel:
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
        city=CityModel(id=user.city.id, name=user.city.name, area_id=user.city.areaId) if user.city else None,
        country=CountryModel(id=user.country.id, name=user.country.name,
                             area_id=user.country.areaId) if user.country else None,
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
        projects=[ProjectModel(id=p.id, name=p.name, description=p.description, link=p.link) for p in user.project],
        achievements=[AchievementModel(id=a.id, name=a.name, description=a.description, link=a.link) for a in
                      user.achievement],
        work_experiences=[
            WorkExperienceModel(
                id=w.id,
                job_id=w.jobId,
                work_place=w.workPlace,
                description=w.description,
                start_date=w.startDate,
                finish_date=w.finishDate,
            )
            for w in user.workexperience
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
        skills=[SkillModel(id=s.id, name=s.name, description=s.description) for s in user.skill],
        languages=[LanguageModel(id=l.id, name=l.name) for l in user.language],
    )


def map_vacancy(vacancy: Vacancy) -> VacancyModel:
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
    )