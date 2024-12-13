from your_job_offer.repository.vacancies_repository.db_methods import (
    get_all_users,
)

from your_job_offer.use_cases.tracking.internal import parse_for_user, log

from your_job_offer.use_cases.user_cases import saveUser
from your_job_offer.utils.mock import get_user
from your_job_offer.use_cases.vacancy_cases import getAllVacancyFromDb


def parse():
    users = get_all_users()
    log.info(f"начинаю обновление статусов, юзеров {len(users)}")
    # for user in users:
    #     parse_for_user(user)
    log.info("закончил обновление статусов")


if __name__ == "__main__":
    # user = get_user()
    # saveUser(user)
    parse()
    # vacancies = getAllVacancyFromDb()
    # for vacancy in vacancies:
    #     print(f"job={vacancy.job}, employer={vacancy.employer}")
