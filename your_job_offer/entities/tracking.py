from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .jobs import VacancyModel


class StatusEnum(Enum):
    CONSIDERATION = "consideration"
    REJECT = "reject"
    INVITE = "invite"  # это значит нужно заполнить какую-то информацию
    TESTING = "testing"
    INTERVIEW = (
        "interview"  # этап invite пройден, нужно записаться на собеседование
    )


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
