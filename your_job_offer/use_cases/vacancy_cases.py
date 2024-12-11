from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods


def getAllVacancyFromDb() -> [VacancyModel]:
    vacancies = db_methods.get_all_vacancies()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.map_vacancy(item))
    return vacanciesModels
