# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
# )
# from sqlalchemy.orm import relationship
#
# from services.vacancies_repository import Base
#
#
# class Country(Base):
#     __tablename__ = "country"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200), nullable=True)
#     areaId = Column(Integer, nullable=True, name="area_id")
#     user = relationship("User", back_populates="country")
#
#
# class City(Base):
#     __tablename__ = "city"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200), nullable=True)
#     areaId = Column(Integer, nullable=True, name="area_id")
#     user = relationship("User", back_populates="city")
#
#
# class Language(Base):
#     __tablename__ = "language"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200), nullable=True)
#     user = relationship(
#         "User",back_populates="language"
#     )
#
#
# class Skill(Base):
#     __tablename__ = "skill"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200), nullable=True)
#     description = Column(String(300), nullable=True)
#     user = relationship("User", back_populates="skill")
#
#
# class Job(Base):
#     __tablename__ = "job"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(200), nullable=True)
#     description = Column(String(300), nullable=True)
#
