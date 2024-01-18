from pydantic import BaseModel, constr, conint, validator
from datetime import datetime
from uuid import UUID

from enums.status import ReservationStatus


def convert_datetime_to_iso_8601(dt: datetime) -> str:
  return dt.strftime('%Y-%m-%d')


class ReservationBase(BaseModel):
  username: constr(max_length=80)
  library_uid: UUID
  book_uid: UUID
  status: ReservationStatus
  start_date: datetime
  till_date: datetime
  
  class Config:
    json_encoders = {
      datetime: convert_datetime_to_iso_8601
    }


class ReservationFilter(BaseModel):
  username: constr(max_length=80) | None = None
  library_uid: UUID | None = None
  book_uid: UUID | None = None
  status: ReservationStatus | None = None
  start_date: datetime | None = None
  till_date: datetime | None = None

  @validator("start_date", "till_date", pre=True)
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)
  

class ReservationUpdate(BaseModel):
  username: constr(max_length=80) | None = None
  library_uid: UUID | None = None
  book_uid: UUID | None = None
  status: ReservationStatus | None = None
  start_date: datetime | None = None
  till_date: datetime | None = None

  @validator("start_date", "till_date", pre=True)
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)


class ReservationCreate(BaseModel):
  username: constr(max_length=80)
  library_uid: UUID
  book_uid: UUID
  status: ReservationStatus
  start_date: datetime
  till_date: datetime

  @validator("start_date", "till_date", pre=True)
  def datetime_validate(cls, dt):
    return datetime.fromisoformat(dt)


class Reservation(ReservationBase):
  id: int
  reservation_uid: UUID
  
