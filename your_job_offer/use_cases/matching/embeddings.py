from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.user import UserModel


def _match_vacancies_by_embeddings(
    vacancies: list[VacancyModel], user: UserModel
) -> list[VacancyModel]:
    pass  # TODO
