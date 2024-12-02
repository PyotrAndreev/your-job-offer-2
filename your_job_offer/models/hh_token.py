from sqlalchemy import Column, Integer, String
from repository.tokens_repository.db_session import Base


class HH_Token(Base):
    __tablename__ = "hh_tokens"
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, name="login")
    access_token = Column(String(512), nullable=False, name="access")
    refresh_token = Column(String(512), nullable=False, name="refresh")
