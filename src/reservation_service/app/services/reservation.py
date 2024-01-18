from click import UUID
from sqlalchemy.orm import Session

from cruds.reservation import ReservationCRUD
from schemas.reservation import ReservationFilter, ReservationUpdate, ReservationCreate
from exceptions.http import NotFoundException, ConflictException
from models.reservation import ReservationModel


class ReservationService():
  def __init__(self, reservationCRUD: ReservationCRUD, db: Session):
    self._reservationCRUD: ReservationCRUD = reservationCRUD(db)

  async def get_all(
      self,
      filter: ReservationFilter,
      page: int = 1,
      size: int = 100,
  ):
    return await self._reservationCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
  
  async def get_by_uid(
      self, 
      uid: UUID,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="get reservation")
    
    return reservation

  async def create(
      self,
      reservation_create: ReservationCreate,
  ):
    reservation = ReservationModel(**reservation_create.model_dump())
    reservation = await self._reservationCRUD.create(reservation)
    if reservation is None:
      raise ConflictException(prefix="create reservation")
    
    return reservation
  
  async def patch(
      self,
      uid: UUID,
      reservation_patch: ReservationUpdate,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="patch reservation")
    
    reservation = await self._reservationCRUD.update(reservation, reservation_patch)
    if reservation is None:
      raise ConflictException(prefix="patch reservation")
    
    return reservation
  
  async def delete(
      self,
      uid: UUID,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="delete reservation")
    
    return await self._reservationCRUD.delete(reservation)
