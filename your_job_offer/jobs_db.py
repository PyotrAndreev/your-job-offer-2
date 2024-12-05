from sqlalchemy import (
    create_engine,
)
from repository.vacancies_repository.db_session import Base

from models.vacancy import Vacancy
from models.user import Country, City, Language, Skill, Job, Education, WorkExperience, User, Project, Achievement

engine = create_engine(
    "postgresql+psycopg2://postgres:password@db:5432/jobs"
)

Base.metadata.create_all(engine)
