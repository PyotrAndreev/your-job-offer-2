from your_job_offer.entities.user import UserModel
from your_job_offer.entities.tracking import (
    StatusModel,
)

from your_job_offer.services.mail_checker.methods import get_email_messages
from your_job_offer.repository.vacancies_repository.db_methods import (
    get_vacancies_by_keys,
)

from .internal import *


def get_all_stages(user: UserModel) -> list[StatusModel]:
    """
    Возвращает все поданные userом заявки
    """
    raw_messages = get_email_messages(user)
    raw_messages = filter_from_spam(raw_messages)
    cleaned_messages = clean_messages(raw_messages)
    parsed_messages = parse_messages(cleaned_messages)
    normal_messages = make_normal_messages(parsed_messages, raw_messages)
    vacancies = get_vacancies_by_keys(
        list(
            map(
                lambda parsed_message: parsed_message.vacancy_key,
                normal_messages,
            )
        ),
        user,
    )
    ans: list[StatusModel] = []
    for vacancy, parsed_message in zip(vacancies, normal_messages):
        if vacancy is not None:
            ans.append(
                StatusModel(
                    vacancy_id=vacancy.id,
                    stage=parsed_message.stage.stage_type,
                    deadline=parsed_message.stage.deadline,
                    date=parsed_message.stage.date,
                    message=parsed_message.stage.message,
                )
            )
    return ans
