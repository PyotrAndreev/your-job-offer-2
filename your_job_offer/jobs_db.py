from sqlalchemy import (
    create_engine,
)
from your_job_offer.repository.vacancies_repository.db_session import Base

# from your_job_offer.models.vacancy import (
#     Vacancy,
#     Status,
#     VacancyStatus,
#     UserVacancy,
# )
# from your_job_offer.models.user import (
#     Country,
#     City,
#     Language,
#     Skill,
#     Job,
#     Education,
#     WorkExperience,
#     User,
#     Project,
#     Achievement,
#     ProfessionalRole,
# )
from your_job_offer.models.vacancy import *
from your_job_offer.models.user import *

# from your_job_offer.repository.vacancies_repository.parsing import parse

engine = create_engine("postgresql+psycopg2://postgres:password@db:5432/jobs")

Base.metadata.create_all(engine)
# if __name__ == "__main__":
#     parse()
