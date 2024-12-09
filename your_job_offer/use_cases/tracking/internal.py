from collections import defaultdict
import string
from dataclasses import replace
import re

import pymorphy2
from bs4 import BeautifulSoup

from your_job_offer.entities.user import EmailMessage
from your_job_offer.entities.tracking import (
    VacancyKey,
    Stage,
    ParsedMessage,
)
from .email_parser import parser


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


def parse_messages(messages: list[EmailMessage]) -> list[ParsedMessage | None]:
    return parser.parse(messages)


def separate_by_vacancy(
    messages: list[ParsedMessage],
) -> dict[VacancyKey, list[Stage]]:
    """
    Разделяет сообщения по ключу вакансии.

    Эта функция принимает список объектов ParsedMessage и группирует их по
    ключу вакансии, возвращая словарь, где ключом является
    VacancyKey, а значением — список этапов (Stage), соответствующих
    каждой вакансии.

    :param messages: Список объектов ParsedMessage, которые необходимо
                     сгруппировать по ключу вакансии.
    :return: Словарь, где ключами являются VacancyKey, а значениями —
             списки этапов, относящихся к каждой вакансии.
    """
    ans = defaultdict(list[Stage])
    for message in messages:
        ans[message.vacancy_key].append(message.stage)
    return ans


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


def make_normal_messages(
    parsed_messages: list[ParsedMessage | None],
    raw_messages: list[EmailMessage],
) -> list[ParsedMessage]:
    if len(parsed_messages) != len(raw_messages):
        raise ValueError(
            f"парсинг не удался, запарсенных сообщений {len(parsed_messages)}, всех { len(raw_messages)}"
        )
    result: list[ParsedMessage] = []
    for parsed_message, raw_message in zip(parsed_messages, raw_messages):
        if (
            parsed_message is not None
            and parsed_message.vacancy_key.employer != ""
            and parsed_message.vacancy_key.job != ""
        ):
            parsed_message.stage.message = raw_message.body
            parsed_message.stage.date = raw_message.date
            result.append(parsed_message)
    return result
