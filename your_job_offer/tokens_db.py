from sqlalchemy import create_engine
from repository.tokens_repository.db_session import Base

engine = create_engine("postgresql+psycopg2://postgres:password@db-tokens:5432/tokens")

Base.metadata.create_all(engine)
