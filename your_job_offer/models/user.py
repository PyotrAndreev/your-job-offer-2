from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from your_job_offer.entities.enums import (
    GenderEnum,
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    RelocationEnum,
    EmploymentEnum,
    ScheduleEnum,
    LanguageLevelEnum,
    EducationLevelEnum,
)
from your_job_offer.repository.vacancies_repository.db_session import Base


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    areaId = Column(Integer, nullable=True, name="area_id")
    user = relationship("User", back_populates="country")


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    areaId = Column(Integer, nullable=True, name="area_id")
    user = relationship("User", back_populates="city")


class Language(Base):
    __tablename__ = "language"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    level = Column(
        PgEnum(LanguageLevelEnum, name="level", create_type=True),
        nullable=True,
    )
    user = relationship(
        "User", secondary="language_user", back_populates="language"
    )


class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)
    user = relationship("User", secondary="skill_user", back_populates="skill")


class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"), name="user_id")
    name = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)
    link = Column(String(200), nullable=True)
    user = relationship("User", back_populates="project", uselist=False)


class Achievement(Base):
    __tablename__ = "achievement"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"), name="user_id")
    name = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)
    link = Column(String(200), nullable=True)
    user = relationship("User", back_populates="achievement", uselist=False)


class WorkExperience(Base):
    __tablename__ = "workExperience"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    jobId = Column(Integer, nullable=True)
    workPlace = Column(String(200), nullable=True, name="work_place")
    description = Column(String(300), nullable=True)
    startDate = Column(Date, nullable=True, name="start_date")
    finishDate = Column(Date, nullable=True, name="finish_date")
    user = relationship("User", back_populates="workExperience")


class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    institution = Column(String(50), nullable=True)
    major = Column(String(50), nullable=True)
    degree = Column(String(50), nullable=True)
    description = Column(String(300), nullable=True)
    startDate = Column(Date, nullable=True, name="start_date")
    finishDate = Column(Date, nullable=True, name="finish_date")
    user = relationship("User", back_populates="education")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, name="login")
    password = Column(String(200), nullable=False, name="password")
    birthDate = Column(String(50), nullable=True, name="birth_date")
    firstName = Column(String(50), nullable=True, name="first_name")
    lastName = Column(String(50), nullable=True, name="last_name")
    middleName = Column(String(50), nullable=True, name="middle_name")
    photo = Column(String(50), nullable=True)
    gender = Column(
        PgEnum(GenderEnum, name="gender", create_type=True), nullable=True
    )
    phone = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    cityId = Column(
        Integer, ForeignKey("city.id"), nullable=True, name="city_id"
    )
    countryId = Column(
        Integer, ForeignKey("country.id"), nullable=True, name="country_id"
    )
    cv = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)
    workType = Column(
        PgEnum(WorkTypeEnum, name="work_type", create_type=True), nullable=True
    )
    minSalary = Column(Integer, nullable=True, name="min_salary")
    maxSalary = Column(Integer, nullable=True, name="max_salary")
    businessTripReadiness = Column(
        PgEnum(
            BusinessTripReadinessEnum,
            name="business_trip_readiness",
            create_type=True,
        ),
        nullable=True,
    )
    workHours = Column(Integer, nullable=True, name="work_hours")
    relocation = Column(
        PgEnum(RelocationEnum, name="relocation", create_type=True),
        nullable=True,
    )
    employment = Column(
        PgEnum(EmploymentEnum, name="employment", create_type=True),
        nullable=True,
    )
    schedule = Column(
        PgEnum(ScheduleEnum, name="schedule", create_type=True), nullable=True
    )
    educationLevel = Column(
        PgEnum(EducationLevelEnum, name="education_level", create_type=True),
        nullable=True,
    )
    hhResumeId = Column(String, name="hh_resume_id", nullable=True)
    innerEmail = Column(String, name="inner_email", nullable=True)
    innerEmailPassword = Column(
        String, name="inner_email_password", nullable=True
    )
    project = relationship("Project", back_populates="user")
    achievement = relationship("Achievement", back_populates="user")
    workExperience = relationship("WorkExperience", back_populates="user")
    education = relationship("Education", back_populates="user")
    skill = relationship(
        "Skill", secondary="skill_user", back_populates="user"
    )
    language = relationship(
        "Language", secondary="language_user", back_populates="user"
    )
    country = relationship("Country", back_populates="user")
    city = relationship("City", back_populates="user")
    vacancy = relationship(
        "Vacancy", secondary="user_vacancy_status", back_populates="user"
    )


class SkillUser(Base):
    __tablename__ = "skill_user"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    skillId = Column(Integer, ForeignKey("skill.id"))


class LanguageUser(Base):
    __tablename__ = "language_user"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    languageId = Column(Integer, ForeignKey("language.id"))
