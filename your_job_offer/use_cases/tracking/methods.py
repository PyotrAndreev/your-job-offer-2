from  entities.user import UserModel
from  entities.tracking import (
    TrackUnit,
)

from  services.mail_checker.methods import get_email_messages
from  repository.vacancies_repository.db_methods import (
    get_vacancies_by_keys,
)

from .internal import *


def get_all_stages(user: UserModel) -> list[TrackUnit]:
    """
    Возвращает все поданные userом заявки
    """
    raw_messages = get_email_messages(user)
    raw_messages = filter_from_spam(raw_messages)
    cleaned_messages = clean_messages(raw_messages)
    parsed_messages = parse_messages(cleaned_messages)
    normal_messages = make_normal_messages(parsed_messages, raw_messages)
    separated_messages = separate_by_vacancy(normal_messages)
    vacancies = get_vacancies_by_keys(list(separated_messages.keys()))
    ans: list[TrackUnit] = []
    for vacancy, stages in zip(vacancies, separated_messages.values()):
        if vacancy is not None:
            ans.append(TrackUnit(vacancy, stages))
    return ans
