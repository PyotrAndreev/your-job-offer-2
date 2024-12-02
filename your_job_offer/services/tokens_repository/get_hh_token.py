from entities.hh_token import HHTokenModel
from services.tokens_repository import db_methods
from services.hh_api.refresh_hh_token import refresh_hh_token


def get_hh_token(login: str) -> HHTokenModel:
    hh_token = db_methods.get_hh_token(login)
    refresh_hh_token(hh_token)
    hh_token = db_methods.get_hh_token(login)
    return hh_token
