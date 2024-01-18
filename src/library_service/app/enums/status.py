from enum import Enum


class ConditionStatus(str, Enum):
  EXCELLENT = 'EXCELLENT'
  GOOD = 'GOOD'
  BAD = 'BAD'
