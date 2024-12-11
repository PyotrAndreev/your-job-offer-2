from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .jobs import VacancyModel
import pandas as pd


class Date(pd.Timestamp):
    def __init__(self, date: str):
        try:
            pd.Timestamp(date)
            super().__init__(date)
        except Exception:
            super().__init__()


class StageEnum(Enum):
    CONSIDERATION = "consideration"
    REJECT = "reject"
    INVITE = "invite"  # это значит нужно заполнить какую-то информацию
    TESTING = "testing"
    INTERVIEW = (
        "interview"  # этап invite пройден, нужно записаться на собеседование
    )


@dataclass
class Stage:
    stage_type: StageEnum
    deadline: Date
    date: Date = Date("")
    message: str = ""


@dataclass
class StatusModel:
    vacancy_id: str
    stage: StageEnum
    deadline: str
    date: str
    message: str


@dataclass(frozen=True)
class VacancyKey:
    job: str
    employer: str
    id_vacancy_from_source: str = ""


@dataclass
class ParsedMessage:
    vacancy_key: VacancyKey
    stage: Stage
