from dataclasses import dataclass
from enum import Enum

from your_job_offer.domain.models.jobs import Vacancy, SourceEnum
from your_job_offer.domain.models.general import Date


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
    message: str
    date: Date


@dataclass
class TrackUnit:  # я не знаю, как еще назвать)
    vacancy: Vacancy
    stages: list[Stage]


@dataclass(frozen=True)
class VacancyKey:
    source: SourceEnum
    id: str
