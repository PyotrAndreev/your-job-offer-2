from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from enums import (
    GenderEnum,
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    RelocationEnum,
    EmploymentEnum,
    ScheduleEnum,
)


@dataclass
class CountryModel:
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"Country(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass
class CityModel:
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"City(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass
class LanguageModel:
    id: int
    name: Optional[str] = None

    def __str__(self):
        return f"Language(id={self.id}, name={self.name})"


@dataclass
class SkillModel:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        return f"Skill(id={self.id}, name={self.name}, description={self.description})"


@dataclass
class ProjectModel:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

    def __str__(self):
        return f"Project(id={self.id}, name={self.name}, description={self.description}, link={self.link})"


@dataclass
class AchievementModel:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

    def __str__(self):
        return f"Achievement(id={self.id}, name={self.name}, description={self.description}, link={self.link})"


@dataclass
class WorkExperienceModel:
    id: int
    job_id: Optional[int] = None
    work_place: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None

    def __str__(self):
        return (
            f"WorkExperience(id={self.id}, job_id={self.job_id}, work_place={self.work_place}, "
            f"description={self.description}, start_date={self.start_date}, finish_date={self.finish_date})"
        )


@dataclass
class EducationModel:
    id: int
    institution: Optional[str] = None
    major: Optional[str] = None
    degree: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None

    def __str__(self):
        return (
            f"Education(id={self.id}, institution={self.institution}, major={self.major}, "
            f"degree={self.degree}, description={self.description}, "
            f"start_date={self.start_date}, finish_date={self.finish_date})"
        )


@dataclass
class UserModel:
    id: int
    login: str
    password: str
    birth_date: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    photo: Optional[str] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[CityModel] = None
    country: Optional[CountryModel] = None
    cv: Optional[str] = None
    description: Optional[str] = None
    work_type: Optional[WorkTypeEnum] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    business_trip_readiness: Optional[BusinessTripReadinessEnum] = None
    work_hours: Optional[int] = None
    relocation: Optional[RelocationEnum] = None
    employment: Optional[EmploymentEnum] = None
    schedule: Optional[ScheduleEnum] = None
    projects: List[ProjectModel] = field(default_factory=list)
    achievements: List[AchievementModel] = field(default_factory=list)
    work_experiences: List[WorkExperienceModel] = field(default_factory=list)
    educations: List[EducationModel] = field(default_factory=list)
    skills: List[SkillModel] = field(default_factory=list)
    languages: List[LanguageModel] = field(default_factory=list)

    def __str__(self):
        return (
            f"User(id={self.id}, login={self.login}, password='***', first_name={self.first_name}, "
            f"last_name={self.last_name}, gender={self.gender}, email={self.email}, city={self.city}, "
            f"country={self.country}, projects={self.projects}, achievements={self.achievements}, "
            f"work_experiences={self.work_experiences}, educations={self.educations}, "
            f"skills={self.skills}, languages={self.languages})"
        )


@dataclass
class VacancyModel:
    id: int
    job: Optional[str] = None
    description: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    address: Optional[str] = None
    link: Optional[str] = None
    apply_link: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    employer: Optional[str] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    work_type: Optional[WorkTypeEnum] = None
    business_trip_readiness: Optional[BusinessTripReadinessEnum] = None
    work_hours: Optional[int] = None
    relocation: Optional[RelocationEnum] = None
    employment: Optional[EmploymentEnum] = None
    schedule: Optional[ScheduleEnum] = None
    has_test: Optional[bool] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    area: Optional[str] = None

    def __str__(self):
        return (
            f"Vacancy(id={self.id}, job={self.job}, description={self.description}, min_salary={self.min_salary}, "
            f"max_salary={self.max_salary}, address={self.address}, employer={self.employer}, "
            f"work_type={self.work_type}, schedule={self.schedule}, requirement={self.requirement})"
        )
