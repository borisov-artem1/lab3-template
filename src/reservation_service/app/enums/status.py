from enum import Enum


class ReservationStatus(str, Enum):
  RENTED = 'RENTED'
  RETURNED = 'RETURNED'
  EXPIRED = 'EXPIRED'
