from collections import defaultdict

from your_job_offer.domain.models.user import User, EmailMessage
from your_job_offer.domain.models.jobs import SourceEnum
from your_job_offer.domain.models.tracking import (
    TrackUnit,
    VacancyKey,
    Stage,
    StageEnum,
)

from your_job_offer.services.mail_checker.methods import get_email_messages
from your_job_offer.services.vacancies_repository.db_methods import get_vacancy

from .hh import (
    get_stage_type_from_hh,
    clean_body_from_hh,
    get_id_from_hh,
    clean_body_from_hh2,
)

MAIL_SOURCES = {
    "=?UTF-8?B?0KDRg9GB0LvQsNC9INCv0YTQsNGA0L7Qsg==?= <afarovruslancrypto@gmail.com>": SourceEnum.HHRU,
    "hh.ru <noreply@hh.ru>": SourceEnum.HHRU,
}


def clean_message(message: EmailMessage) -> None:
    """
    удаляет все лишнее
    """
    if MAIL_SOURCES[message.sender] == SourceEnum.HHRU:
        message.body = clean_body_from_hh(message)


def clean_message2(message: EmailMessage) -> None:
    """
    Удаляет ссылку на вакансию и остальную ненужную информацию
    """
    if MAIL_SOURCES[message.sender] == SourceEnum.HHRU:
        message.body = clean_body_from_hh2(message)


def filter_and_clean_messages(
    messages: list[EmailMessage],
) -> list[EmailMessage]:
    answer: list[EmailMessage] = []
    for message in messages:
        if message.sender in MAIL_SOURCES.keys():
            clean_message(message)
            if message.body != "":
                answer.append(message)
    return answer


def get_id(source: SourceEnum, message: EmailMessage) -> str:
    if source == SourceEnum.HHRU:
        return get_id_from_hh(message)


def get_vancancy_key(message: EmailMessage) -> VacancyKey:
    source = MAIL_SOURCES[message.sender]
    id = get_id(source, message)
    return VacancyKey(source, id)


def get_stage_type(source: SourceEnum, message: EmailMessage) -> StageEnum:
    if source == SourceEnum.HHRU:
        return get_stage_type_from_hh(message)


def separate_by_vacancy(
    messages: list[EmailMessage],
) -> dict[VacancyKey, list[EmailMessage]]:
    ans = defaultdict(list[EmailMessage])
    for message in messages:
        ans[get_vancancy_key(message)].append(message)
    return ans


def get_all_stages(user: User) -> list[TrackUnit]:
    email_messages = get_email_messages(user)
    email_messages = filter_and_clean_messages(email_messages)
    separated_messages = separate_by_vacancy(email_messages)
    ans: list[TrackUnit] = []
    for vacancy_key, messages in separated_messages.items():
        vacancy = get_vacancy(vacancy_key)
        stages: list[Stage] = []
        for message in messages:
            stage_type = get_stage_type(vacancy_key.source, message)
            clean_message2(message)
            stages.append(
                Stage(
                    stage_type,
                    message.body,
                    message.date,
                )
            )
        ans.append(TrackUnit(vacancy, stages))
    return ans
