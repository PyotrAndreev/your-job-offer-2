from dataclasses import dataclass
from typing import Optional

from .enums import StatusEnum


@dataclass
class StatusModel:
    id: Optional[int] = None
    status: Optional[StatusEnum] = None
    deadline: Optional[str] = None
    date: Optional[str] = None
    message: Optional[str] = None


@dataclass(frozen=True)
class VacancyKey:
    job: str
    employer: str
    id_vacancy_from_source: str = ""


@dataclass
class ParsedMessage:
    vacancy_key: VacancyKey
    status: StatusModel
