from enum import Enum

class WorkTypeEnum(Enum):
    OFFICE = 'office'
    REMOTE = 'remote'
    HYBRID = 'hybrid'
    FIELD_WORK = 'field_work'

class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'

class BusinessTripReadinessEnum(Enum):
    READY = 'ready'
    SOMETIMES = 'sometimes'
    NEVER = 'never'

class RelocationEnum(Enum):
    NO = 'no'
    POSSIBLE = 'possible'
    DESIRABLE = 'desirable'

class EmploymentEnum(Enum):
    FULL = 'full'
    PART = 'part'
    PROJECT = 'project'
    VOLUNTEER = 'volunteer'
    PROBATION = 'probation'

class ScheduleEnum(Enum):
    FULL_DAY = 'full_day'
    SHIFT = 'shift'
    FLEXIBLE = 'flexible'
    REMOTE = 'remote'
    FLY_IN_FLY_OUT = 'fly_in_fly_out'
