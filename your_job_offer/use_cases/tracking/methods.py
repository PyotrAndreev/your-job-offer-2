# from your_job_offer.use_cases.user_cases import (
#     get_all_users,
# )

# from your_job_offer.use_cases.tracking.internal import parse_for_user, log

# from your_job_offer.use_cases.user_cases import saveUser, updateUser
# from your_job_offer.utils.mock import get_user
# from your_job_offer.use_cases.vacancy_cases import getAllVacancyFromDb
# from your_job_offer.repository.vacancies_repository import db_methods
# from your_job_offer.models.vacancy import Status
# from time import sleep
# from your_job_offer.entities.tracking import StatusModel, StatusEnum


# def parse():
#     users = get_all_users()
#     log.info(f"начинаю обновление статусов, юзеров {len(users)}")
#     for user in users:
#         # parse_for_user(user)
#         for vacancy in user.vacancy:
#             vacancy_ = db_methods.get_vacancy_by_id(vacancy.id)
#             vacancy_.status.append(Status(statusField=StatusEnum.REJECT))
#             log.info(f"job={vacancy.job}, employer={vacancy.employer}")
#         # statuss = get_all_statuses(user)
#         # for status in statuss:
#         #     log.info(status.status)
#         #     log.info(status.date)
#         #     log.info(status.deadline)
#         #     log.info(status.message[: min(300, len(status.message))])
#     # users = get_all_users()
#     # for user in users:
#     #     log.info(user.vacancy)
#     log.info("закончил обновление статусов")


# if __name__ == "__main__":
#     user = get_user()
#     parse()
#     # vacancies = getAllVacancyFromDb()
#     # for vacancy in vacancies:
#     #     log.info(f"job={vacancy.job}, employer={vacancy.employer}")

from your_job_offer.repository.vacancies_repository.db_session import session
from your_job_offer.models.vacancy import Vacancy, Status, StatusEnum
from your_job_offer.models.user import User
from sqlalchemy import select

# from your_job_offer.repository.vacancies_repository.parsing import parse

# vacancies = [
#     Vacancy(description="1"),
#     Vacancy(description="2"),
#     Vacancy(description="3"),
# ]

# # Добавляем и сохраняем вакансии в таблицу `vacancy`
# for vacancy in vacancies:
#     session.add(vacancy)
# session.commit()  # Фиксируем изменения, чтобы данные сохранились в БД
# parse()

# Проверяем ID вакансий, если нужно (опционально)
vacancies = session.execute(select(Vacancy)).scalars().all()
while len(vacancies) < 50:
    vacancies = session.execute(select(Vacancy)).scalars().all()
vacancy_1 = vacancies[0]

# Создаём пользователя
user = User(login="ruslan", password="123")

# Добавляем связь между пользователем и вакансиями (1 и 3)
user.vacancy = vacancies

# Сохраняем пользователя в базу данных
session.add(user)
session.commit()  # Фиксируем изменения

user = session.execute(select(User)).scalars().all()[0]
print(*[vacancy.job for vacancy in user.vacancy])


# user = session.query(User).filter_by(login="ruslan").first()
# vacancy = session.query(Vacancy).filter_by(description="3").first()
# user.vacancy.append(vacancy)
# session.commit()

user = session.execute(select(User)).scalars().all()[0]
print(*[vacancy.description for vacancy in user.vacancy])

vacancy_id = vacancy_1.id

vacancy = session.get(Vacancy, vacancy_id)
statuses = [
    Status(message="1", statusField=StatusEnum("consideration")),
    Status(message="2", statusField=StatusEnum.REJECT),
]
for status in statuses:
    vacancy.status.append(Status(statusField=StatusEnum.REJECT))
session.commit()

vacancy = session.get(Vacancy, vacancy_id)
for status in vacancy.status:
    print(status.message, status.statusField)

# посмотреть mapperы
