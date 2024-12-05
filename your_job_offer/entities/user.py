from dataclasses import dataclass, field
import re
from datetime import date
from typing import Optional, List
from dataclasses_json import dataclass_json

from entities.enums import WorkTypeEnum, BusinessTripReadinessEnum, EmploymentEnum, RelocationEnum, ScheduleEnum, \
    GenderEnum
from entities.general import SkillModel, LanguageModel, CityModel, CountryModel


@dataclass_json
@dataclass
class Name:
    name: str

    def __post_init__(self):
        if not re.match(
                "[A-zА-я]{2,25}", self.name
        ):  # наверное, если строка пришла какая-то не такая, то лучше
            # оставить поле пустым и пусть пользователь сам заполнит
            self.name = ""


@dataclass_json
@dataclass
class ProjectModel:
    """
    Represents a project associated with a user.

    Attributes:
        id (int): The unique identifier of the project.
        name (Optional[str]): The name of the project.
        description (Optional[str]): A brief description of the project.
        link (Optional[str]): A link to the project.

    Methods:
        __str__: Returns a string representation of the ProjectModel instance.
    """
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

    def __str__(self):
        return f"Project(id={self.id}, name={self.name}, description={self.description}, link={self.link})"


@dataclass_json
@dataclass
class AchievementModel:
    """
    Represents an achievement associated with a user.

    Attributes:
        id (int): The unique identifier of the achievement.
        name (Optional[str]): The name of the achievement.
        description (Optional[str]): A brief description of the achievement.
        link (Optional[str]): A link to the achievement.

    Methods:
        __str__: Returns a string representation of the AchievementModel instance.
    """
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None

    def __str__(self):
        return f"Achievement(id={self.id}, name={self.name}, description={self.description}, link={self.link})"


@dataclass_json
@dataclass
class WorkExperienceModel:
    """
    Represents a user's work experience.

    Attributes:
        id (int): The unique identifier of the work experience entry.
        job_id (Optional[int]): The job identifier related to the work experience.
        work_place (Optional[str]): The company or organization where the user worked.
        description (Optional[str]): A brief description of the work performed.
        start_date (Optional[date]): The date when the work experience started.
        finish_date (Optional[date]): The date when the work experience ended.

    Methods:
        __str__: Returns a string representation of the WorkExperienceModel instance.
    """
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


@dataclass_json
@dataclass
class EducationModel:
    """
    Represents a user's education.

    Attributes:
        id (int): The unique identifier of the education entry.
        institution (Optional[str]): The name of the institution where the user studied.
        major (Optional[str]): The major or field of study.
        degree (Optional[str]): The degree obtained.
        description (Optional[str]): A brief description of the education.
        start_date (Optional[date]): The start date of the education.
        finish_date (Optional[date]): The finish date of the education.

    Methods:
        __str__: Returns a string representation of the EducationModel instance.
    """
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


@dataclass_json
@dataclass
class UserModel:
    """
    Represents a user profile with various personal and professional details.

    Attributes:
        id (int): The unique identifier of the user.
        login (str): The login of the user.
        password (str): The password of the user.
        birth_date (Optional[str]): The birthdate of the user.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
        middle_name (Optional[str]): The middle name of the user.
        photo (Optional[str]): A link to the user's photo.
        gender (Optional[GenderEnum]): The gender of the user.
        phone (Optional[str]): The user's phone number.
        email (Optional[str]): The user's email address.
        city (Optional[CityModel]): The city where the user is located.
        country (Optional[CountryModel]): The country where the user is located.
        cv (Optional[str]): A link to the user's CV.
        description (Optional[str]): A brief description about the user.
        work_type (Optional[WorkTypeEnum]): The preferred work type of the user.
        min_salary (Optional[int]): The minimum salary the user expects.
        max_salary (Optional[int]): The maximum salary the user expects.
        business_trip_readiness (Optional[BusinessTripReadinessEnum]): The user's readiness for business trips.
        work_hours (Optional[int]): The user's preferred working hours.
        relocation (Optional[RelocationEnum]): The user's willingness to relocate.
        employment (Optional[EmploymentEnum]): The user's preferred employment type.
        schedule (Optional[ScheduleEnum]): The user's preferred work schedule.
        projects (List[ProjectModel]): A list of projects associated with the user.
        achievements (List[AchievementModel]): A list of achievements associated with the user.
        work_experiences (List[WorkExperienceModel]): A list of work experiences of the user.
        educations (List[EducationModel]): A list of education entries for the user.
        skills (List[SkillModel]): A list of skills the user possesses.
        languages (List[LanguageModel]): A list of languages the user knows.

    Methods:
        __str__: Returns a string representation of the UserModel instance.
    """
    login: str
    password: str
    id: Optional[int] = None
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


@dataclass_json
@dataclass
class EmailMessage:
    sender: str = ""
    date: str = ""
    header: str = ""
    body: str = ""
