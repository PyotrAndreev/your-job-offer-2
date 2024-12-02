import re
from string import punctuation
from operator import itemgetter

import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import download as nltk_download
from pymorphy2 import MorphAnalyzer

from entities.jobs import VacancyModel
from entities.user import UserModel

punctuation = punctuation.replace("+", "")  # чтобы не ликвидировать C++


class TextPreprocessor:
    def __init__(self):
        nltk_download("punkt_tab")
        nltk_download("stopwords")
        rus_stops = stopwords.words("russian")
        self.filter_token = rus_stops + [
            "знание",
            "способность",
            "умение",
            "высокий",
            "уровень",
            "степень",
            "опыт",
            "хороший",
            "практический",
            "навык",
            "качество",
            "год",
            "мидло",
            "понимание",
            "концепция",
            "некоторый",
        ]
        self.parser = MorphAnalyzer()

    @staticmethod
    def clean(word: str) -> str:
        return re.sub(r"[^A-ZА-Яa-zа-я+\s]", "", word)

    def lemmatize(self, word: str) -> str:
        return self.parser.parse(word)[0].normal_form

    def text_to_tokens(self, text: str) -> list[str]:
        text = text.lower()
        text = text.translate(
            str.maketrans(punctuation, " " * len(punctuation))
        )
        text = text.translate(str.maketrans({"\n": " ", "\t": " ", "-": " "}))
        tokenized_text = word_tokenize(text)
        clean_text = list(map(self.clean, tokenized_text))
        lemmatized_text = []
        for word in clean_text:
            word = self.lemmatize(word)
            if not (
                len(word) < 2 or word in self.filter_token
            ):  # однобуквенные слова смысла не несут
                lemmatized_text.append(word)
        return lemmatized_text


def isin(skills: list[str], requirement: str | None) -> int:
    if requirement is None or len(requirement) == 0:
        return 1
    ans = 0
    for skill in skills:
        if skill in requirement:
            ans += 1
    return ans


def _match_vacancies_by_word_entry(
    vacancies: list[VacancyModel], user: UserModel
) -> list[VacancyModel]:
    """
    [Baseline]
    проверяет, что хотя бы один скилл из user входит в хотя бы одно слово из requirement
    """
    processor = TextPreprocessor()
    user_skills = list(
        map(
            lambda skill: " ".join(processor.text_to_tokens(skill)),
            user.skills,
        )
    )
    counts_isin = np.array(
        list(
            map(
                lambda vacancy: isin(user_skills, vacancy.requirement),
                vacancies,
            )
        )
    )

    indexes = np.argsort(
        counts_isin,
    )[
        ::-1
    ][: sum(counts_isin != 0)]

    return itemgetter(*indexes)(vacancies)
