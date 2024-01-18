from enum import Enum


class ConditionStatus(str, Enum):
  EXCELLENT = 'EXCELLENT'
  GOOD = 'GOOD'
  BAD = 'BAD'


class ReservationStatus(str, Enum):
  RENTED = 'RENTED'
  RETURNED = 'RETURNED'
  EXPIRED = 'EXPIRED'
