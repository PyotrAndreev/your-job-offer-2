from sqlalchemy import create_engine
from your_job_offer.repository.tokens_repository.db_session import Base
from your_job_offer.models.hh_token import HH_Token

engine = create_engine(
    "postgresql+psycopg2://postgres:password@db-tokens:5432/tokens"
)

Base.metadata.create_all(engine)
