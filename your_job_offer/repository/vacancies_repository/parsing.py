from .hh_get_vacancies import hh_get_vacancies


def parse() -> None:
    all_sources_get_vacancies = [hh_get_vacancies]
    parsed_vacancies = []
    for get_vacancies in all_sources_get_vacancies:
        parsed_vacancies.extend(get_vacancies())
    db_vacancies = get_all_vacancies_db()
    new = get_new_vacancies(parsed_vacancies, db_vacancies)
    for vacancy in new:
        save_vacancy(vacancy)


if __name__ == "__main__":
    parse()
