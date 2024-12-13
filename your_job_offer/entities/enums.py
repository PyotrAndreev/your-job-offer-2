from enum import Enum
import dataclasses_json


@dataclasses_json
class WorkTypeEnum(Enum):
    OFFICE = "office"
    REMOTE = "remote"
    HYBRID = "hybrid"
    FIELD_WORK = "field_work"

@dataclasses_json
class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"

@dataclasses_json
class BusinessTripReadinessEnum(Enum):
    READY = "ready"
    SOMETIMES = "sometimes"
    NEVER = "never"

@dataclasses_json
class RelocationEnum(Enum):
    NO = "no_relocation"
    POSSIBLE = "relocation_possible"
    DESIRABLE = "relocation_desirable"

@dataclasses_json
class EmploymentEnum(Enum):
    FULL = "full"
    PART = "part"
    PROJECT = "project"
    VOLUNTEER = "volunteer"
    PROBATION = "probation"

@dataclasses_json
class ScheduleEnum(Enum):
    FULL_DAY = "fullDay"
    SHIFT = "shift"
    FLEXIBLE = "flexible"
    REMOTE = "remote"
    FLY_IN_FLY_OUT = "flyInFlyOut"

@dataclasses_json
class LanguageLevelEnum(Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"
    L1 = "l1"

@dataclasses_json
class EducationLevelEnum(Enum):
    SECONDARY = "secondary"
    SPECIAL_SECONDARY = "special_secondary"
    UNFINISHED_HIGHER = "unfinished_higher"
    HIGHER = "higher"
    BACHELOR = "bachelor"
    MASTER = "master"
    CANDIDATE = "candidate"
    DOCTOR = "doctor"

@dataclasses_json
class SourceEnum(Enum):
    HH_RU = "hh.ru"
    UNK = "unknown"

@dataclasses_json
class StageEnum(Enum):
    CONSIDERATION = "consideration"
    REJECT = "reject"
    INVITE = "invite"  # это значит нужно заполнить какую-то информацию или записаться на собеседование
    TESTING = "testing"
    INTERVIEW = (
        "interview"  # этап invite пройден, нужно записаться на собеседование
    )

@dataclasses_json
class CitizenshipEnum(Enum):
    rf = "rf"
    another = "another"
