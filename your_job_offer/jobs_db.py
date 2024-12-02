from sqlalchemy import (
    create_engine,
)
from repository.vacancies_repository.db_session import Base

engine = create_engine(
    "postgresql+psycopg2://postgres:password@db:5432/jobs"
)

Base.metadata.create_all(engine)
