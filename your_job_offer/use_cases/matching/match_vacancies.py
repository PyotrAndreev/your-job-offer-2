from enum import Enum

from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.user import UserModel
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods
from .word_entry import _match_vacancies_by_word_entry
from .embeddings import _match_vacancies_by_embeddings


class MatchingEnum(Enum):
    WORD_ENTRY = "word_entry"
    EMBEDDINGS = "embeddings"


def filter_without_skills(
    vacancies: list[VacancyModel], user: UserModel
) -> list[VacancyModel]:
    """
    фильтрует то, что не смогли отфильтровать по запросам к бд, но без учёта скиллов,
    то есть поля area, experience
    """
    if user.relocation:
        return vacancies
    return vacancies  # TODO


def match_vacancies(
    vacancies: list[VacancyModel],
    user: UserModel,
    mode: MatchingEnum = MatchingEnum.WORD_ENTRY,
) -> list[VacancyModel]:
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


def get_match_vacancies(user: UserModel) -> list[VacancyModel]:
    vacancies = db_methods.get_vacancies_by_user(mapper.map_userModel(user))
    list_vac = []
    for item in vacancies:
        list_vac.append(mapper.map_vacancy(item))
    # list_vac = match_vacancies(list_vac, user)
    return list_vac[:10]
