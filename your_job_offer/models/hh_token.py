from sqlalchemy import Column, Integer, String
from repository.tokens_repository.db_session import Base


class HH_Token(Base):
    """
    Represents a user's token information for authentication with hh.ru.

    This class is mapped to the 'hh_tokens' table in the database, which stores the login and
    associated access and refresh tokens for authentication purposes.

    Attributes:
        id (int): The unique identifier of the token entry (Primary Key).
        login (str): The login associated with the token.
        access_token (str): The access token used for authentication with the hh.ru API.
        refresh_token (str): The refresh token used to obtain a new access token when the old one expires.
    """
    __tablename__ = "hh_tokens"
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, name="login")
    access_token = Column(String(512), nullable=False, name="access")
    refresh_token = Column(String(512), nullable=False, name="refresh")
