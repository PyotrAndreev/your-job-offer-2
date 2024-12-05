import logger
from entities.hh_token import HHTokenModel
from repository.tokens_repository import db_methods
from services.hh_api.refresh_hh_token import refresh_hh_token

log = logger.get_logger(__name__)


def get_hh_token(login: str) -> HHTokenModel:
    """
    Retrieves the HH token for a given user login. If the token is expired or not found,
    it refreshes the token and retrieves it again.

    Args:
        login (str): The user's login for which to retrieve the HH token.

    Returns:
        HHTokenModel: The HH token object associated with the provided login.

    """
    hh_token = db_methods.get_hh_token(login)
    refresh_hh_token(hh_token)
    hh_token = db_methods.get_hh_token(login)
    return hh_token
