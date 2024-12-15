from enum import Enum


class WorkTypeEnum(Enum):
    OFFICE = "office"
    REMOTE = "remote"
    HYBRID = "hybrid"
    FIELD_WORK = "field_work"


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"


class BusinessTripReadinessEnum(Enum):
    READY = "ready"
    SOMETIMES = "sometimes"
    NEVER = "never"


class RelocationEnum(Enum):
    NO = "no_relocation"
    POSSIBLE = "relocation_possible"
    DESIRABLE = "relocation_desirable"


class EmploymentEnum(Enum):
    FULL = "full"
    PART = "part"
    PROJECT = "project"
    VOLUNTEER = "volunteer"
    PROBATION = "probation"


class ScheduleEnum(Enum):
    FULL_DAY = "fullDay"
    SHIFT = "shift"
    FLEXIBLE = "flexible"
    REMOTE = "remote"
    FLY_IN_FLY_OUT = "flyInFlyOut"


class LanguageLevelEnum(Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"
    L1 = "l1"


class EducationLevelEnum(Enum):
    SECONDARY = "secondary"
    SPECIAL_SECONDARY = "special_secondary"
    UNFINISHED_HIGHER = "unfinished_higher"
    HIGHER = "higher"
    BACHELOR = "bachelor"
    MASTER = "master"
    CANDIDATE = "candidate"
    DOCTOR = "doctor"


class SourceEnum(Enum):
    HH_RU = "hh.ru"
    UNK = "unknown"


class StatusEnum(Enum):
    CONSIDERATION = "consideration"
    REJECT = "reject"
    INVITE = "invite"  # это значит нужно заполнить какую-то информацию или записаться на собеседование
    TESTING = "testing"
    INTERVIEW = (
        "interview"  # этап invite пройден, нужно записаться на собеседование
    )


class CitizenshipEnum(Enum):
    rf = "rf"
    another = "another"
