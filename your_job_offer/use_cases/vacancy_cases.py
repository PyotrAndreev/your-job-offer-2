from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.tracking import StatusModel
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods


def getAllVacancyFromDb() -> list[VacancyModel]:
    vacancies = db_methods.get_all_vacancies()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.map_vacancy(item))
    return vacanciesModels


def update_status(status: StatusModel):
    vacancy = db_methods.get_vacancy_by_id(status.vacancy_id)
    vacancy.status.append(mapper.map_status_model(status))
    db_methods.session.commit()
