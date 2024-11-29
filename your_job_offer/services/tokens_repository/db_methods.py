from models.hh_token import HH_Token
from services.tokens_repository.db_session import session


def save_token(token: HH_Token):
    session.add(token)
    session.commit()