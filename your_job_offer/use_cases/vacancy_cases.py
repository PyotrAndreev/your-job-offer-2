from your_job_offer.entities.jobs import VacancyModel
from your_job_offer.entities.tracking import StatusModel, StatusEnum
from your_job_offer.mappers import mapper
from your_job_offer.repository.vacancies_repository import db_methods
from your_job_offer.models.vacancy import Status


def getAllVacancyFromDb() -> list[VacancyModel]:
    vacancies = db_methods.get_all_vacancies()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.map_vacancy(item))
    return vacanciesModels


def update_statuses(vacancy_ids: list[int], statuses: list[StatusModel]):
    for vacancy_id, status in zip(vacancy_ids, statuses):
        # print(status.vacancy_id)
        vacancy = db_methods.get_vacancy_by_id(vacancy_id)
        status.status = StatusEnum.REJECT
        # vacancy.status.append(mapper.map_status_model(status))
        print(StatusEnum.__members__)
        vacancy.status.append(Status(statusField=StatusEnum.REJECT))
    db_methods.session.commit()
