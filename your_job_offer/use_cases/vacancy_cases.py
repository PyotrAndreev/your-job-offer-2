from entities.jobs import VacancyModel
from mappers import mapper
from repository.vacancies_repository import db_methods


def getAllVacancyFromDb()->[VacancyModel]:
    vacancies=db_methods.get_all_vacancies()
    vacanciesModels = []
    for item in vacancies:
        vacanciesModels.append(mapper.map_vacancy(item))
    return vacanciesModels

