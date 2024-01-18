from sqlalchemy.orm import Session, Query
from uuid import UUID

from schemas.reservation import ReservationFilter, ReservationUpdate
from models.reservation import ReservationModel


class ReservationCRUD():
  def __init__(self, db: Session):
    self._db = db

  async def get_all(
      self,
      filter: ReservationFilter,
      offset: int = 0,
      limit: int = 100,
  ) -> list[ReservationModel]:
    reservations = self._db.query(ReservationModel)
    reservations = await self.__filter_reservations(reservations, filter)
    return reservations.offset(offset).limit(limit).all()
  
  async def get_by_uid(self, uid: UUID) -> ReservationModel | None:
    return self._db.query(ReservationModel).filter(ReservationModel.reservation_uid == uid).first()
  
  async def create(self, reservation: ReservationModel) -> ReservationModel | None:
    try:
      self._db.add(reservation)
      self._db.commit()
      self._db.refresh(reservation)
    except:
      return None
    
    return reservation
  
  async def update(self, reservation: ReservationModel, reservation_update: ReservationUpdate) -> ReservationModel | None:
    update_fields = reservation_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
      setattr(reservation, key, value)

    try:
      self._db.add(reservation)
      self._db.commit()
      self._db.refresh(reservation)
    except:
      return None
    
    return reservation
  
  async def delete(self, reservation: ReservationModel) -> ReservationModel:
    self._db.delete(reservation)
    self._db.commit()

    return reservation

  async def __filter_reservations(
      self,
      reservations: Query[ReservationModel],
      filter: ReservationFilter
    ) -> Query[ReservationModel]:
    if filter.username:
      reservations = reservations.filter(ReservationModel.username == filter.username)

    if filter.book_uid:
      reservations = reservations.filter(ReservationModel.book_uid == filter.book_uid)
    
    if filter.library_uid:
      reservations = reservations.filter(ReservationModel.library_uid == filter.library_uid)

    if filter.status:
      reservations = reservations.filter(ReservationModel.status == filter.status)

    if filter.start_date:
      reservations = reservations.filter(ReservationModel.start_date == filter.start_date)

    if filter.till_date:
      reservations = reservations.filter(ReservationModel.till_date == filter.till_date)

    return reservations
