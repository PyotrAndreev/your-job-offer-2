from your_job_offer.repository.vacancies_repository.hh_get_vacancies import (
    get_vacancies as hh_get_vacancies,
)
from your_job_offer.repository.vacancies_repository.db_methods import (
    get_all_vacancies,
    save_vacancy,
)


from your_job_offer.models.vacancy import Vacancy
from your_job_offer.mappers.mapper import (
    map_vacancy_db_to_vacancy_key,
    VacancyKey,
)
from typing import Iterable


def vacancies_to_dict(
    vacancies: list[Vacancy],
) -> dict[VacancyKey, Vacancy]:
    result = {}
    for vacancy in vacancies:
        result[map_vacancy_db_to_vacancy_key(vacancy)] = vacancy
    return result


def filter_vacancies(
    filter_keys: set[VacancyKey], vacancies_dict: dict[VacancyKey, Vacancy]
) -> list[Vacancy]:
    return list(map(lambda key: vacancies_dict[key], filter_keys))


# TODO сделать обновление описания, пометить устаревшие вакансии, что делать,
# если из разных источников одни и те же вакансии
def get_new_vacancies(
    parsed_vacancies: Iterable[Vacancy], db_vacancies: Iterable[Vacancy]
) -> list[Vacancy]:
    """
    Определяет, какие вакансии новые
    """
    db_vacancies_dict = vacancies_to_dict(db_vacancies)
    parsed_vacancies_dict = vacancies_to_dict(parsed_vacancies)
    db_vacancies_keys = set(db_vacancies_dict.keys())
    parsed_vacancies_keys = set(parsed_vacancies_dict.keys())
    new_keys = parsed_vacancies_keys - db_vacancies_keys
    outdated_keys = db_vacancies_keys - parsed_vacancies_keys
    new = filter_vacancies(new_keys, parsed_vacancies_dict)
    outdated = filter_vacancies(outdated_keys, db_vacancies_dict)
    # TODO outdated
    return new


def parse() -> None:
    all_sources_get_vacancies = [hh_get_vacancies]
    parsed_vacancies = []
    for get_vacancies in all_sources_get_vacancies:
        parsed_vacancies.extend(get_vacancies())
    db_vacancies = get_all_vacancies()
    new = get_new_vacancies(parsed_vacancies, db_vacancies)
    for vacancy in new:
        save_vacancy(vacancy)


if __name__ == "__main__":
    parse()
