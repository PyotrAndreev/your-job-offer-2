from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5431/jobs')
Session = sessionmaker(bind=engine)
session = Session()