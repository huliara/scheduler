from enum import Enum


class ShiftState(Enum):
    before_hiring = 0
    hiring = 1
    decide_assignees = 2
    archive = 3
