from enum import Enum


from your_job_offer.domain.models.jobs import Vacancy
from your_job_offer.domain.models.user import User

from .word_entry import _match_vacancies_by_word_entry
from .embeddings import _match_vacancies_by_embeddings


class MatchingEnum(Enum):
    WORD_ENTRY = "word_entry"
    EMBEDDINGS = "embeddings"


def match_vacancies(
    vacancies: list[Vacancy],
    user: User,
    mode: MatchingEnum = MatchingEnum.WORD_ENTRY,
) -> list[Vacancy]:
    if mode == MatchingEnum.EMBEDDINGS:
        return _match_vacancies_by_embeddings(vacancies, user)
    return _match_vacancies_by_word_entry(vacancies, user)
