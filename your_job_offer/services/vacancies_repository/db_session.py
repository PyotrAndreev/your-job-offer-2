from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:password@db:5432/jobs')
Session = sessionmaker(bind=engine)
session = Session()