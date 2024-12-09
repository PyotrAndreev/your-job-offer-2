from dataclasses import dataclass
from enum import Enum

from entities.jobs import VacancyModel
import pandas as pd


class SourceEnum(Enum):
    HH_RU = "hh.ru"
    UNK = "unknown"


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
    INVITE = "invite"  # это значит нужно заполнить какую-то информацию или записаться на собеседование
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
class TrackUnit:  # я не знаю, как еще назвать)
    vacancy: VacancyModel
    stages: list[Stage]


@dataclass(frozen=True)
class VacancyKey:
    job: str
    employer: str
    id: str = ""


@dataclass
class ParsedMessage:
    vacancy_key: VacancyKey
    stage: Stage
