from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship

from your_job_offer.entities.enums import (
    WorkTypeEnum,
    BusinessTripReadinessEnum,
    ScheduleEnum,
    EmploymentEnum,
    RelocationEnum,
    SourceEnum,
    StatusEnum,
)
from your_job_offer.repository.vacancies_repository.db_session import Base


class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(Integer, primary_key=True)
    job = Column(String(200), nullable=True)
    description = Column(String(300), nullable=True)
    minSalary = Column(Integer, nullable=True, name="min_salary")
    maxSalary = Column(Integer, nullable=True, name="max_salary")
    address = Column(String(200), nullable=True)
    link = Column(String(200), nullable=True)
    applyLink = Column(String(200), nullable=True, name="apply_link")
    phone = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    employer = Column(String(200), nullable=True)
    createdAt = Column(String(50), nullable=True, name="created_at")
    updatedAt = Column(String(50), nullable=True, name="updated_at")
    workType = Column(
        PgEnum(WorkTypeEnum, name="work_type", create_type=True), nullable=True
    )
    businessTripReadiness = Column(
        PgEnum(
            BusinessTripReadinessEnum,
            name="business_trip_readiness",
            create_type=True,
        ),
        nullable=True,
    )
    workHours = Column(Integer, nullable=True, name="work_hours")
    relocation = Column(
        PgEnum(RelocationEnum, name="relocation", create_type=True),
        nullable=True,
    )
    employment = Column(
        PgEnum(EmploymentEnum, name="employment", create_type=True),
        nullable=True,
    )
    schedule = Column(
        PgEnum(ScheduleEnum, name="schedule", create_type=True), nullable=True
    )
    hasTest = Column(Boolean, nullable=True, name="has_test")
    requirement = Column(String, nullable=True, name="requirement")
    responsibility = Column(String, nullable=True, name="responsibility")
    area = Column(String(200), nullable=True)
    professionalRoleId = Column(
        Integer, nullable=True, name="proffesional_role_id"
    )
    source = Column(
        PgEnum(SourceEnum, name="source", create_type=True), nullable=True
    )
    idVacancyFromSource = Column(
        String, nullable=True, name="id_vacancy_from_source"
    )


class UserStatus(Base):
    __tablename__ = "user_status"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    statusId = Column(Integer, ForeignKey("status.id"))


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    statusField = Column(
        PgEnum(StatusEnum, name="status_field", create_type=True),
        nullable=True,
    )
    deadline = Column(String, nullable=True, name="deadline")
    date = Column(String, nullable=True, name="date")
    message = Column(String, nullable=True, name="message")
    vacancy = relationship(
        "Vacancy", secondary="vacancy_status", back_populates="status"
    )
    user = relationship(
        "User", secondary="user_status", back_populates="status"
    )

class VacancyStatus(Base):
    __tablename__ = "vacancy_status"
    id = Column(Integer, primary_key=True)
    vacancyId = Column(Integer, ForeignKey("vacancy.id"))
    statusId = Column(Integer, ForeignKey("status.id"))
