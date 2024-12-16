from dataclasses import dataclass
from typing import Optional

from .enums import StatusEnum
from your_job_offer.entities.jobs import VacancyModel


@dataclass
class StatusModel:
    id: Optional[int] = None
    status: Optional[StatusEnum] = None
    deadline: Optional[str] = None
    date: Optional[str] = None
    message: Optional[str] = None
    vacancy: Optional[VacancyModel] = None


@dataclass(frozen=True)
class VacancyKey:
    job: str
    employer: str
    id_vacancy_from_source: str = ""


@dataclass
class ParsedMessage:
    vacancy_key: VacancyKey
    status: StatusModel
