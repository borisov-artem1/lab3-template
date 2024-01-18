from uuid import UUID
from models.reservation import ReservationModel
from schemas.reservation import ReservationFilter
from cruds.mocks.data import ReservationMockData


class ReservationMockCRUD(ReservationMockData):
  def __init__(self, db):
        self._db = db
        
  async def get_all(
      self,
      filter: ReservationFilter,
      offset: int = 0,
      limit: int = 100
    ):
    
    reservations = [
      ReservationModel(**item) for item in self._reservations
    ]
    reservations = await self.__filter_reservations(reservations, filter)
  
    return reservations[offset:limit]
  
  async def get_by_uid(self, reservation_uid: UUID):
    for item in self._reservations:
      if item["reservation_uid"] == str(reservation_uid):
        return ReservationModel(**item)
      
    return None
  
  async def create(self, reservation: ReservationModel):  
    self._reservations.append(
      {
        "id": 1 if len(self._reservations) == 0 
            else self._reservations[-1]["id"] + 1,
        "username": reservation.username,
        "library_uid": reservation.library_uid,
        "book_uid": reservation.book_uid,
        "status": reservation.status,
        "start_date": reservation.start_date,
        "till_date": reservation.till_date,
        "reservation_uid": reservation.reservation_uid,
      },
    )
    
    return ReservationModel(**self._reservations[-1])

  async def delete(self, reservation: ReservationModel):
    for i in range(len(self._reservations)):
      item = self._reservations[i]
      if item["reservation_uid"] == reservation.reservation_uid:
        deleted_reservation = self._reservations.pop(i)
        break

    return ReservationModel(**deleted_reservation)
  
  async def __filter_reservations(self, reservations, reservation_filter: ReservationFilter):
    return reservations
