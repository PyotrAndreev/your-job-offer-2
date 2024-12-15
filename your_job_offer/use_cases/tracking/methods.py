from your_job_offer.use_cases.user_cases import (
    get_all_users,
)

from your_job_offer.use_cases.tracking.internal import parse_for_user, log

from your_job_offer.use_cases.user_cases import saveUser, updateUser
from your_job_offer.utils.mock import get_user
from your_job_offer.use_cases.vacancy_cases import getAllVacancyFromDb
from time import sleep


def parse():
    users = get_all_users()
    log.info(f"начинаю обновление статусов, юзеров {len(users)}")
    for user in users:
        parse_for_user(user)
        for vacancy in user.vacancy:
            #     log.info(vacancy)
            log.info(f"job={vacancy.job}, employer={vacancy.employer}")
        # statuss = get_all_statuses(user)
        # for status in statuss:
        #     log.info(status.status)
        #     log.info(status.date)
        #     log.info(status.deadline)
        #     log.info(status.message[: min(300, len(status.message))])
    # users = get_all_users()
    # for user in users:
    #     log.info(user.vacancy)
    log.info("закончил обновление статусов")


if __name__ == "__main__":
    user = get_user()
    parse()
    # vacancies = getAllVacancyFromDb()
    # for vacancy in vacancies:
    #     log.info(f"job={vacancy.job}, employer={vacancy.employer}")
