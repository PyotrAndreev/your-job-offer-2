from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5431/jobs')

Base = declarative_base()


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


class WorkType(Base):
    __tablename__ = 'work_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    vacancy = relationship('Vacancy', back_populates='work_type')


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    jobId = Column(Integer, ForeignKey('job.id'), name='job_id')
    description = Column(String(300), nullable=True)
    workTypeId = Column(Integer, ForeignKey('work_type.id'), name='work_type_id')
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
    businessTripReadiness = Column(Boolean, nullable=True, name='business_trip_readiness')
    workHours = Column(Integer, nullable=True, name='work_hours')
    relocation = Column(Boolean, nullable=True)
    hasTest = Column(Boolean, nullable=True, name='has_test')
    workType = relationship('WorkType', back_populates='vacancy')
    job = relationship('Job', back_populates='vacancy')
    skill = relationship('Skill', back_populates='vacancy')


class SkillVacancy(Base):
    __tablename__ = 'skill_vacancy'
    id = Column(Integer, primary_key=True)
    vacancyId = Column(Integer, ForeignKey('vacancy.id'))
    skillId = Column(Integer, ForeignKey('skill.id'))

Base.metadata.create_all(engine)



