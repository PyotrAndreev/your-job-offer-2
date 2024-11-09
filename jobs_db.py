from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from enums import *

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5431/jobs')

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    areaId = Column(Integer, nullable=False, name='area_id')
    areaName = Column(String, nullable=False, name='area_name')
    vacancy = relationship('Vacancy', back_populates='country')


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    areaId = Column(Integer, nullable=False, name='area_id')
    areaName = Column(String, nullable=False, name='area_name')
    vacancy = relationship('Vacancy', back_populates='city')


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    skill = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    vacancy = relationship('Vacancy', secondary='skill_vacancy', back_populates='skill')


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    job = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    vacancy = relationship('Vacancy', back_populates='job')


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    jobId = Column(Integer, ForeignKey('job.id'), name='job_id')
    description = Column(String(300), nullable=True)
    minSalary = Column(Integer, nullable=True, name='min_salary')
    maxSalary = Column(Integer, nullable=True, name='max_salary')
    address = Column(String(50), nullable=True)
    link = Column(String(50), nullable=False)
    applyLink = Column(String(50), nullable=False, name='apply_link')
    phone = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    employer = Column(String(50), nullable=True)
    createdAt = Column(Date, nullable=False, name='created_at')
    updatedAt = Column(Date, nullable=True, name='updated_at')
    workType = Column(PgEnum(WorkTypeEnum, name='work_type', create_type=True), nullable=False)
    businessTripReadiness = Column(PgEnum(BusinessTripReadinessEnum, name='business_trip_readiness', create_type=True),
                                   nullable=False)
    workHours = Column(Integer, nullable=True, name='work_hours')
    relocation = Column(PgEnum(RelocationEnum, name='relocation', create_type=True), nullable=True)
    employment = Column(PgEnum(EmploymentEnum, name='employment', create_type=True), nullable=True)
    schedule = Column(PgEnum(ScheduleEnum, name='schedule', create_type=True), nullable=True)
    hasTest = Column(Boolean, nullable=True, name='has_test')
    cityId = Column(Integer, ForeignKey('city.id'), name='city_id')
    countryId = Column(Integer, ForeignKey('country.id'), name='country_id')

    job = relationship('Job', back_populates='vacancy')
    skill = relationship('Skill', back_populates='vacancy')
    country = relationship('Country', back_populates='vacancy')
    city = relationship('City', back_populates='vacancy')


class SkillVacancy(Base):
    __tablename__ = 'skill_vacancy'
    id = Column(Integer, primary_key=True)
    vacancyId = Column(Integer, ForeignKey('vacancy.id'))
    skillId = Column(Integer, ForeignKey('skill.id'))


Base.metadata.create_all(engine)
