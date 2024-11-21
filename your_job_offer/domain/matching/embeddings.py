from your_job_offer.domain.models.jobs import Vacancy
from your_job_offer.domain.models.user import User


def _match_vacancies_by_embeddings(
    vacancies: list[Vacancy], user: User
) -> list[Vacancy]:
    pass  # TODO
