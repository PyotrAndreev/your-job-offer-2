import re

from your_job_offer.domain.models.user import EmailMessage
from your_job_offer.domain.models.tracking import (
    StageEnum,
)


def clean_body_from_hh(message: EmailMessage) -> str:
    if not (
        "с вами хотят" in message.header.lower()
        or "сообщение от работадателя" in message.header.lower()
        or "работадатель не готов" in message.header.lower()
        or "пройдите тестирование" not in message.header.lower()
    ):
        return ""
    lines = message.body.split("\n")
    begin_first_line = "<http"
    last_line = "Вопросы и ответы\r"
    first_ind = -1
    for i, line in enumerate(lines):
        if (
            first_ind < 0
            and len(line) >= len(begin_first_line)
            and line[: len(begin_first_line)] == begin_first_line
        ):
            first_ind = i + 1
        if line == last_line:
            last_ind = i - 1
    message_lines = [
        line[:-1] for line in lines[first_ind:last_ind] if line != "\r"
    ]
    return " ".join(message_lines)


def clean_body_from_hh2(message: EmailMessage) -> str:
    index = message.body.find("Вакансия:")
    return message.body[:index]


def get_stage_type_from_hh(message: EmailMessage) -> StageEnum:
    if "хотят" in str(message.header.lower()):
        return StageEnum.INVITE
    if "готов" in str(message.header.lower()):
        return StageEnum.REJECT
    if "тестирование" in str(message.header.lower()):
        return StageEnum.TESTING
    return StageEnum.CONSIDERATION


def find_url(s: str) -> str:
    pattern = r"ссылке <(.*?)>"
    matches = re.findall(pattern, s)
    return matches[-1]


def find_vacancy_number(s):
    start_index = s.find("vacancy/") + len("vacancy/")
    vacancy_number = ""
    for char in s[start_index:]:
        if char.isdigit():
            vacancy_number += char
        else:
            break
    return vacancy_number


def get_id_from_hh(message: EmailMessage) -> str:
    return find_vacancy_number(find_url(message.body))
