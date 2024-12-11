from your_job_offer.entities.user import UserModel
from your_job_offer.models.user import User
from your_job_offer.repository.vacancies_repository import db_methods
from your_job_offer.mappers import mapper


def getUser(login: str) -> UserModel:
    user = db_methods.get_user(login=login)
    return mapper.map_user(user)


def saveUser(user: UserModel) -> UserModel:
    user = db_methods.save_user(mapper.map_userModel(user))
    return mapper.map_user(user)


def updateUser(user: UserModel) -> UserModel:
    return db_methods.update_user(mapper.map_userModel(user))


def ifExistUser(login: str) -> bool:
    return db_methods.if_exist_user(login=login)
