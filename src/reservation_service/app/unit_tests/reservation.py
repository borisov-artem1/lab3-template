from copy import deepcopy
from datetime import datetime as dt

from cruds.mocks.reservation import ReservationMockCRUD
from cruds.mocks.data import ReservationMockData
from services.reservation import ReservationService
from schemas.reservation import ReservationFilter, ReservationCreate
from models.reservation import ReservationModel
from exceptions.http import NotFoundException, ConflictException


reservationService = ReservationService(
  reservationCRUD=ReservationMockCRUD,
  db=None,
)
correct_reservations = deepcopy(ReservationMockData._reservations)


def model_into_dict(model: ReservationModel) -> dict:
  dictionary = model.__dict__
  del dictionary["_sa_instance_state"]
  return dictionary


async def test_get_all_reservations_success():
  try:
    reservations = await reservationService.get_all(
      filter=ReservationFilter()
    )

    assert len(reservations) == len(correct_reservations)
    for i in range(len(reservations)):
      assert model_into_dict(reservations[i]) == correct_reservations[i]
  except:
    assert False


async def test_get_reservation_by_uid_success():
  try:
    reservation = await reservationService.get_by_uid("00000000-0000-0000-0000-000000000031")

    assert model_into_dict(reservation) == correct_reservations[0]
  except:
    assert False


async def test_get_reservation_by_uid_not_found():
  try:
    await reservationService.get_by_uid(10)

    assert False
  except NotFoundException:
    assert True
  except:
    assert False


async def test_add_reservation_success():
  try:
    reservation = await reservationService.create(
      ReservationCreate(
        username="test",
        library_uid="00000000-0000-0000-0000-000000000111",
        book_uid="00000000-0000-0000-0000-000000000121",
        status="RENTED",
        start_date="2024-01-18",
        till_date="2024-01-18",
      )
    )
    
    assert \
      reservation.username == "test" and \
      str(reservation.library_uid) == "00000000-0000-0000-0000-000000000111" and \
      str(reservation.book_uid) == "00000000-0000-0000-0000-000000000121" and \
      reservation.status == "RENTED" and \
      reservation.start_date.strftime('%Y-%m-%d') == "2024-01-18" and \
      reservation.till_date.strftime('%Y-%m-%d') == "2024-01-18"
  except:
    assert False

async def test_delete_reservation_success():
  try:
    reservation = await reservationService.delete("00000000-0000-0000-0000-000000000033")

    assert correct_reservations[2] == model_into_dict(reservation)
  except:
    assert False


async def test_delete_reservation_not_found():
  try:
    await reservationService.delete(10)
    
    assert False
  except NotFoundException:
    assert True
  except:
    assert False
