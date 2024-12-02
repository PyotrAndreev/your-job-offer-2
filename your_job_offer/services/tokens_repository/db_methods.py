from sqlalchemy.exc import NoResultFound

import logger
from entities.hh_token import HHTokenModel
from mappers.mapper import map_token
from models.hh_token import HH_Token
from services.tokens_repository.db_session import session

log = logger.get_logger(__name__)


def save_hh_token(token: HH_Token):
    session.add(token)
    session.commit()


def get_hh_token(login: str) -> HHTokenModel:
    token = session.query(HH_Token).filter_by(login=login).one()
    return map_token(token)


def update_hh_token(hh_token: HHTokenModel):
    try:
        hh_token_db = session.query(HH_Token).filter_by(login=hh_token.login).one()
        setattr(hh_token_db, "access_token", hh_token.access_token)
        setattr(hh_token_db, "refresh_token", hh_token.refresh_token)
        save_hh_token(hh_token_db)
        log.info(f"Токен hh.ru для пользователя с логином '{hh_token.login}' обновлен")
    except NoResultFound:
        log.warning(f"Пользователь с логином '{hh_token.login}' не найден.")
    except Exception as e:
        log.error(f"Ошибка обновления: {e}")
        session.rollback()
