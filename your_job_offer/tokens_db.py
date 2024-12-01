from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.hh_token import HH_Token
from services.tokens_repository.db_session import Base

engine = create_engine("postgresql+psycopg2://postgres:password@db-tokens:5432/tokens")

Base.metadata.create_all(engine)
