import string
from dataclasses import replace
import re
from typing import Optional

import pymorphy2
from bs4 import BeautifulSoup

from your_job_offer.logger import get_logger
from your_job_offer.entities.user import EmailMessage
from your_job_offer.entities.tracking import (
    VacancyKey,
    ParsedMessage,
)
from your_job_offer.entities.user import UserModel
from your_job_offer.entities.tracking import StatusModel
from your_job_offer.use_cases.user_cases import get_vacancies_by_keys
from your_job_offer.use_cases.vacancy_cases import update_statuses
from your_job_offer.services.mail_checker.methods import get_email_messages
from .email_parser import parser

log = get_logger("vacancy_status_parsing")


def preprocess_text(text):
    # Инициализация морфологического анализатора
    morph = pymorphy2.MorphAnalyzer()

    # Удаление знаков препинания
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Приведение текста к нижнему регистру
    text = text.lower()

    # Лемматизация
    words = text.split()
    lemmatized_words = [morph.parse(word)[0].normal_form for word in words]

    # Возврат нормализованного текста
    return " ".join(lemmatized_words)


def check_words_in_text(words, text):
    text = preprocess_text(text)
    for word in words:
        if word in text:
            return True
    return False


def filter_from_spam(messages: list[EmailMessage]) -> list[EmailMessage]:
    """
    каким-то образом понимает, точно ли письмо спам или ну так, непонятно,
    может спам а может нет
    """
    keywords = [
        "вакансия",
        "работодатель",
        "компания",
        "работа",
        "offer",
        "interview",
        "vacancy",
        "job",
        "positon",
        "company",
    ]
    filtered: list[EmailMessage] = []
    for message in messages:
        if check_words_in_text(
            keywords, message.header
        ) or check_words_in_text(keywords, message.body):
            filtered.append(message)
    return filtered


def parse_messages(
    messages: list[EmailMessage],
) -> list[Optional[ParsedMessage]]:
    return parser.parse(messages)


def clean_text(text):
    # Удаляем HTML-теги
    clean_html = BeautifulSoup(text, "lxml").text

    # Удаляем URL
    clean_text = re.sub(r"http[s]?://S+|www\.S+", "", clean_html)
    clean_text = clean_text.replace("<", "").replace(">", "")
    return re.sub(r"\s+", " ", clean_text)


def clean_messages(messages: list[EmailMessage]) -> list[EmailMessage]:
    """
    Очищает сообщения в письмах от html тегов и т.п
    """
    result: list[EmailMessage] = []
    for message in messages:
        result.append(replace(message))
        result[-1].body = clean_text(result[-1].body)
    return result


def find_vacancy_number(message: EmailMessage) -> Optional[str]:
    """
    Find vacancy id
    """
    s = message.body
    start_index = s.find("vacancy/")
    if start_index == -1:
        return None
    start_index += len("vacancy/")
    vacancy_number = ""
    for char in s[start_index:]:
        if char.isdigit():
            vacancy_number += char
        else:
            break
    return vacancy_number


def make_normal_messages(
    parsed_messages: list[Optional[ParsedMessage]],
    raw_messages: list[EmailMessage],
) -> list[ParsedMessage]:
    if len(parsed_messages) != len(raw_messages):
        raise ValueError(
            f"парсинг не удался, запарсенных сообщений {len(parsed_messages)}, всех { len(raw_messages)}"
        )
    result: list[ParsedMessage] = []
    for parsed_message, raw_message in zip(parsed_messages, raw_messages):
        if parsed_message is not None and (
            parsed_message.vacancy_key.employer != ""
            and parsed_message.vacancy_key.job != ""
            or parsed_message.vacancy_key.id_vacancy_from_source != ""
        ):
            parsed_message.status.message = raw_message.body
            parsed_message.status.date = raw_message.date
            result.append(
                ParsedMessage(
                    vacancy_key=VacancyKey(
                        job=parsed_message.vacancy_key.job,
                        employer=parsed_message.vacancy_key.employer,
                        id_vacancy_from_source=find_vacancy_number(
                            raw_message
                        ),
                    ),
                    status=parsed_message.status,
                )
            )
    return result


def get_parsed_messages(user: UserModel) -> list[ParsedMessage]:
    """
    Возвращает все поданные userом заявки
    """
    raw_messages = get_email_messages(user)
    raw_messages = filter_from_spam(raw_messages)
    cleaned_messages = clean_messages(raw_messages)
    parsed_messages = parse_messages(cleaned_messages)
    normal_messages = make_normal_messages(parsed_messages, raw_messages)
    return normal_messages


def parse_for_user(user: UserModel):
    parsed_messages = get_parsed_messages(user)
    vacancies = get_vacancies_by_keys(
        list(
            map(
                lambda parsed_message: parsed_message.vacancy_key,
                parsed_messages,
            )
        ),
        user,
    )
    for messge, vacancy in zip(parsed_messages, vacancies):
        log.info(messge.vacancy_key)
        if vacancy is None:
            log.info(None)
        else:
            log.info(
                f"id={vacancy.id}, job={vacancy.job}, employer={vacancy.employer}"
            )
    statuses: list[StatusModel] = []
    vacancy_ids = []
    for vacancy, parsed_message in zip(vacancies, parsed_messages):
        if vacancy is not None:
            statuses.append(
                StatusModel(
                    status=parsed_message.status.status,
                    deadline=parsed_message.status.deadline,
                    date=parsed_message.status.date,
                    message=parsed_message.status.message,
                )
            )
            vacancy_ids.append(vacancy.id)
    # for status in statuses:
    #     log.info(status.vacancy_id)
    #     log.info(status.status)
    #     log.info(status.date)
    #     log.info(status.deadline)
    #     log.info(status.message[: min(100, len(status.message))])
    log.info(
        f"user {user.login} подавался на {len(user.vacancy)} вакансий, найдено {len(statuses)} статусов"
    )
    update_statuses(vacancy_ids, statuses)
