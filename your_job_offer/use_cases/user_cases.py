from entities.user import UserModel
from models.user import User
from repository.vacancies_repository import db_methods
from mappers import mapper


def getUser(login: str, password: str) -> UserModel:
    user = db_methods.get_user(login=login, password=password)
    return mapper.map_user(user)


def saveUser(user: UserModel) -> UserModel:
    return db_methods.save_user(mapper.map_userModel(user))


def updateUser(user: UserModel) -> UserModel:
    return db_methods.update_user(user)


def ifExistUser(login: str) -> bool:
    return db_methods.if_exist_user(login=login)
