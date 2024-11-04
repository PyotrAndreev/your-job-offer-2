from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5430/users')

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=False)
    user = relationship('User', back_populates='country')


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    user = relationship('User',  back_populates='city')


class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    language = Column(String(50), nullable=False)
    user = relationship('User', secondary='language_user', back_populates='language')


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    skill = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    user = relationship('User', secondary='skill_user', back_populates='skill')


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    job = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    user = relationship('User', secondary='job_user', back_populates='job')


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'), name='user_id')
    title = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    link = Column(String(50), nullable=True)
    user = relationship('User', back_populates='projects')


class Achievement(Base):
    __tablename__ = 'achievement'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'), name='user_id')
    title = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)
    link = Column(String(50), nullable=True)
    user = relationship('User', back_populates='achievement')


class WorkType(Base):
    __tablename__ = 'work_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    workPreference = relationship('WorkPreference', back_populates='work_type')


class WorkPreference(Base):
    __tablename__ = 'work_preference'
    id = Column(Integer, primary_key=True)
    workTypeId = Column(Integer, ForeignKey('work_type.id'), name='work_type_id')
    minSalary = Column(Integer, nullable=True, name='min_salary')
    maxSalary = Column(Integer, nullable=True, name='max_salary')
    businessTripReadiness = Column(Boolean, nullable=True, name='business_trip_readiness')
    workHours = Column(Integer, nullable=True, name='work_hours')
    relocation = Column(Boolean, nullable=True)
    workType = relationship('WorkType', back_populates='work_preference')
    user = relationship('User', back_populates='work_preference')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    birthDate = Column(String(50), nullable=False, name='birth_date')
    firstName = Column(String(50), nullable=False, name='first_name')
    lastName = Column(String(50), nullable=False, name='last_name')
    middleName = Column(String(50), nullable=True, name='middle_name')
    photo = Column(String(50), nullable=True)
    gender = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cityId = Column(Integer, ForeignKey('city.id'), name='city_id')
    countryId = Column(Integer, ForeignKey('country.id'), name='country_id')
    csv = Column(String(50), nullable=True)
    description = Column(String(300), nullable=True)
    workPreferenceId = Column(Integer, ForeignKey('work_preference.id'), name='work_preference_id')
    workPreference = relationship('WorkPreference', back_populates='user')
    project = relationship('Project', back_populates='user')
    achievement = relationship('Achievement', back_populates='user')
    workExperience = relationship('WorkExperience', back_populates='user')
    education = relationship('Education', back_populates='user')
    skill = relationship('Skill', secondary='skill_user', back_populates='user')
    job = relationship('Job', secondary='job_user', back_populates='user')
    language = relationship('Language', secondary='language_user', back_populates='user')
    country = relationship('Country', back_populates='user')
    city = relationship('City', back_populates='user')


class WorkExperience(Base):
    __tablename__ = 'work_experience'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    jobId = Column(Integer, nullable=False)
    workPlace = Column(String(50), nullable=True, name='work_place')
    description = Column(String(300), nullable=True)
    startDate = Column(Date, nullable=False, name='start_date')
    finishDate = Column(Date, nullable=True, name='finish_date')
    user = relationship('User', back_populates='work_experience')


class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    institution = Column(String(50), nullable=False)
    major = Column(String(50), nullable=True)
    degree = Column(String(50), nullable=True)
    description = Column(String(300), nullable=True)
    startDate = Column(Date, nullable=False, name='start_date')
    finishDate = Column(Date, nullable=True, name='finish_date')
    user = relationship('User', back_populates='education')


class SkillUser(Base):
    __tablename__ = 'skill_user'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    skillId = Column(Integer, ForeignKey('skill.id'))


class JobUser(Base):
    __tablename__ = 'job_user'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    jobId = Column(Integer, ForeignKey('job.id'))


class LanguageUser(Base):
    __tablename__ = 'language_user'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    languageId = Column(Integer, ForeignKey('language.id'))


Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()
#
# user1 = User(name='John Doe', email='john.doe@example.com')
# session.add(user1)
# session.commit()
# country
# session.add(post1)
# session.commit()

