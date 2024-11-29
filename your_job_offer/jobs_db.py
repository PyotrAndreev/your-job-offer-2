from sqlalchemy import (
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from models.vacancy import Vacancy
from models.user import Country, City, Language, Skill, Job, Education, Workexperience, User, Project, Achievement
from services.vacancies_repository.db_session import Base

engine = create_engine(
    "postgresql+psycopg2://postgres:password@db:5432/jobs"
)

Base.metadata.create_all(engine)
