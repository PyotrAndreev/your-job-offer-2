from your_job_offer.use_cases.user_cases import get_all_users
from your_job_offer.use_cases.tracking.internal import parse_for_user, log


def parse():
    users = get_all_users()
    log.info(f"начинаю обновление статусов, юзеров {len(users)}")
    for user in users:
        try:
            parse_for_user(user)
        except Exception:
            log.exception(f"у user={user.login} проблемы с парсингом: ")
    log.info("закончил обновление статусов")


if __name__ == "__main__":
    parse()
