from your_job_offer.models.user import Job, ProfessionalRole
from sqlalchemy import select, or_
from your_job_offer.repository.vacancies_repository.db_session import session



def get_job(job_id: int) -> Job:
    job = session.scalars(select(Job).filter_by(id=job_id)).first()
    return job


def get_job_id(name: str) -> int:
    job = session.scalars(select(Job).filter_by(name=name)).first()
    return job


def get_professional_role(role_id: int) -> ProfessionalRole:
    role = session.scalars(
        select(ProfessionalRole).filter_by(roleId=role_id)
    ).first()
    return role