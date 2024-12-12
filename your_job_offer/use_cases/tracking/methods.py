from your_job_offer.repository.vacancies_repository.db_methods import (
    get_all_users,
)

from .internal import parse_for_user, log


def parse():
    log.info("начинаю обновление статусов")
    for user in get_all_users():
        parse_for_user(user)
    log.info("закончил обновление статусов")


if __name__ == "__main__":
    parse()
