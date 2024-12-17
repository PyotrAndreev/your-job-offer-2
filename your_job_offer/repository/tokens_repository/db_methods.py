from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

import your_job_offer.logger as logger
from your_job_offer.entities.hh_token import HHTokenModel
from your_job_offer.mappers.mapper import map_hh_token
from your_job_offer.models.hh_token import HH_Token
from your_job_offer.repository.tokens_repository.db_session import session

log = logger.get_logger(__name__)


def save_hh_token(hh_token: HH_Token):
    """
    Saves a new HH token to the database.

    Args:
        token (HH_Token): The HH token object to save.

    """
    try:
        session.add(hh_token)
        session.commit()
        log.info(
            f"Токен hh.ru для пользователя с логином '{hh_token.login}' добавлен"
        )
    except Exception as e:
        log.error(f"Ошибка добавления токена: {e}")


def get_hh_token(login: str) -> HHTokenModel:
    """
    Retrieves the HH token for a given user login from the database.

    Args:
        login (str): The user's login for which to retrieve the HH token.

    Returns:
        HHTokenModel: The HH token model object associated with the provided login.

    """
    try:
        hh_token = session.query(HH_Token).filter_by(login=login).one()
        return map_hh_token(hh_token)
    except NoResultFound:
        log.warning(
            f"Токен hh.ru для пользователя с логином {login} не найден"
        )
    except Exception as e:
        log.error(f"Ошибка получения токена: {e}")


def update_hh_token(hh_token: HHTokenModel):
    """
    Updates the HH token in the database for a given user. If the user is not found, logs a warning.

    Args:
        hh_token (HHTokenModel): The updated HH token model to save.

    """
    try:
        hh_token_db = (
            session.query(HH_Token).filter_by(login=hh_token.login).one()
        )
        setattr(hh_token_db, "access_token", hh_token.access_token)
        setattr(hh_token_db, "refresh_token", hh_token.refresh_token)
        save_hh_token(hh_token_db)
        log.info(
            f"Токен hh.ru для пользователя с логином '{hh_token.login}' обновлен"
        )
    except NoResultFound:
        log.warning(
            f"Токен hh.ru для пользователя с логином '{hh_token.login}' не найден."
        )
    except Exception as e:
        log.error(f"Ошибка обновления: {e}")
        session.rollback()
