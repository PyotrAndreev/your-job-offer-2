from enum import Enum


from your_job_offer.domain.models.jobs import Vacancy
from your_job_offer.domain.models.user import User

from .word_entry import _match_vacancies_by_word_entry
from .embeddings import _match_vacancies_by_embeddings


class MatchingEnum(Enum):
    WORD_ENTRY = "word_entry"
    EMBEDDINGS = "embeddings"


def filter_without_skills(
    vacancies: list[Vacancy], user: User
) -> list[Vacancy]:
    """
    фильтрует то, что не смогли отфильтровать по запросам к бд, но без учёта скиллов,
    то есть поля area, experience
    """
    if user.relocation:
        return vacancies
    return vacancies  # TODO


def match_vacancies(
    vacancies: list[Vacancy],
    user: User,
    mode: MatchingEnum = MatchingEnum.WORD_ENTRY,
) -> list[Vacancy]:
    """
    подбирает вакансии по mode, и отсортировывает их по релевантности

    :param vacancies: отфильтрованные по полям employment, schedule, buisiness_trip_readiness, relocation, min_salary вакансии
    :param mode: способ подбора
    :return: список отсортированных вакансий
    """
    vacancies = list(filter(lambda x: x.requirement is not None, vacancies))
    vacancies = filter_without_skills(vacancies, user)
    if mode == MatchingEnum.EMBEDDINGS:
        return _match_vacancies_by_embeddings(vacancies, user)
    return _match_vacancies_by_word_entry(vacancies, user)
