import json
from uuid import UUID
import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings
from schemas.reservation import Reservation, ReservationCreate, ReservationUpdate
from enums.status import ReservationStatus


class ReservationCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    reservation_host = settings["services"]["gateway"]["reservation_host"]
    reservation_port = settings["services"]["reservation"]["port"]

    self.http_path = f'http://{reservation_host}:{reservation_port}/api/v1/'


  async def get_all_reservations(
      self,
      page: int = 1,
      size: int = 100,
      username: str | None = None,
      status: ReservationStatus | None = None,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}reservation/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}'\
        f'{f"&status={status}" if status else ""}'
    )
    self._check_status_code(response.status_code)

    reservation_json: list[Reservation] = response.json()

    reservations: list[Reservation] = []
    for reservation in reservation_json:
      reservations.append(
        Reservation(
          reservationUid=reservation["reservation_uid"],
          username=reservation["username"],
          bookUid=reservation["book_uid"],
          libraryUid=reservation["library_uid"],
          status=reservation["status"],
          startDate=reservation["start_date"],
          tillDate=reservation["till_date"],
        )
      )
    
    return reservations
    

  async def get_reservation_by_uid(
      self,
      uid: UUID,
  ) -> Reservation:
    response: Response = requests.get(
      url=f'{self.http_path}reservation/{uid}'
    )
    self._check_status_code(response.status_code)
    
    reservation = response.json()
    
    return Reservation(
      reservationUid=reservation["reservation_uid"],
      username=reservation["username"],
      bookUid=reservation["book_uid"],
      libraryUid=reservation["library_uid"],
      status=reservation["status"],
      startDate=reservation["start_date"],
      tillDate=reservation["till_date"],
    )
  

  async def patch_reservation(
      self,
      uid: UUID,
      update: ReservationUpdate,
  ):
    update.book_uid = None if not update.book_uid else str(update.book_uid) # is not JSON serializable
    update.library_uid = None if not update.library_uid else str(update.library_uid) # is not JSON serializable
    update.start_date = None if not update.start_date else update.start_date.strftime('%Y-%m-%d') # is not JSON serializable
    update.till_date = None if not update.till_date  else update.till_date.strftime('%Y-%m-%d') # is not JSON serializable

    print(update)

    response: Response = requests.patch(
      url=f'{self.http_path}reservation/{uid}',
      data=json.dumps(update.model_dump(mode='json', exclude_unset=True, exclude_none=True))
    )
    self._check_status_code(response.status_code)

    reservation = response.json()
    return reservation["id"]
  

  async def add_reservation(
      self,
      create: ReservationCreate,
  ) -> UUID:
    create.book_uid = str(create.book_uid) # is not JSON serializable
    create.library_uid = str(create.library_uid) # is not JSON serializable
    create.start_date = create.start_date.strftime('%Y-%m-%d') # is not JSON serializable
    create.till_date = create.till_date.strftime('%Y-%m-%d') # is not JSON serializable

    response: Response = requests.post(
      url=f'{self.http_path}reservation/',
      data=json.dumps(create.model_dump())
    )
    self._check_status_code(response.status_code)

    location: str = response.headers["location"]
    uid = str(location.split("/")[-1])

    return uid
