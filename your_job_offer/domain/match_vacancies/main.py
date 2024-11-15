from enum import Enum

from your_job_offer.domain.models.jobs import Vacancy
from your_job_offer.domain.models.user import User


class MatchingEnum(Enum):
    EMBEDDINGS = "embeddings"
    FILTERS = "filters"


def match_vacancies(
    vacancies: list[Vacancy],
    user: User,
    mode: MatchingEnum = MatchingEnum.EMBEDDINGS,
) -> list[Vacancy]:
    if mode == MatchingEnum.EMBEDDINGS:
        return _match_vacancies_by_embeddings(vacancies, user)
    return _match_vacancies_by_filters(vacancies, user)


def _match_vacancies_by_embeddings(
    vacancies: list[Vacancy], user: User
) -> list[Vacancy]:
    pass


def _match_vacancies_by_filters(
    vacancies: list[Vacancy], user: User
) -> list[Vacancy]:
    pass
