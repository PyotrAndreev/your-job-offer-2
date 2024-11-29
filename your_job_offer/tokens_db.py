from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.hh_token import HH_Token
from services.tokens_repository.db_session import Base

engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5430/tokens")

Base.metadata.create_all(engine)
