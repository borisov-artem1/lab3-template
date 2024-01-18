import json
from uuid import UUID
import sys
from datetime import datetime
import requests

from cruds.library import LibraryCRUD
from cruds.reservation import ReservationCRUD
from cruds.rating import RatingCRUD
from schemas.library import (
  LibraryResponse,
  LibraryPaginationResponse,
  BookInfo,
  LibraryBookEntityResponse,
  LibraryBookResponse,
  LibraryBookPaginationResponse,
  LibraryBookUpdate,
  BookUpdate,
)
from schemas.reservation import (
  Reservation,
  BookReservationResponse,
  TakeBookRequest,
  ReservationCreate,
  TakeBookResponse,
  ReturnBookRequest,
  ReservationUpdate,
)
from schemas.rating import (
  Rating,
  UserRatingResponse,
  RatingUpdate,
  RatingCreate,
)
from utils.requests_queue import RequestQueue
from utils.settings import get_settings
from enums.status import ReservationStatus, ConditionStatus
from exceptions.http import BadRequestException, NotFoundException, ServiceUnavailableException


from copy import deepcopy

class GatewayService():
  def __init__(
      self,
      libraryCRUD: LibraryCRUD,
      reservationCRUD: ReservationCRUD,
      ratingCRUD: RatingCRUD,
  ):
    self._libraryCRUD: LibraryCRUD = libraryCRUD()
    self._reservationCRUD: ReservationCRUD = reservationCRUD()
    self._ratingCRUD: RatingCRUD = ratingCRUD()

    settings = get_settings()
    gateway_host = settings["services"]["gateway"]["host"]
    gateway_port = settings["services"]["gateway"]["port"]
    self.http_path = f'http://{gateway_host}:{gateway_port}/api/v1/'


  async def get_all_libraries_in_city(
      self,
      city: str,
      page: int = 1,
      size: int = 100,
  ):
    libraries = await self._libraryCRUD.get_all_libraries(
      page=page,
      size=size,
      city=city,
    )

    return LibraryPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=libraries.totalElements,
      items=libraries.items,
    )
  

  async def get_books_in_library(
      self,
      library_uid: UUID,
      show_all: bool = False,
      page: int = 1,
      size: int = 100,
  ):
    library_books = await self._libraryCRUD.get_all_library_books(
      page=page,
      size=size,
    )

    library_book_items: list[LibraryBookResponse] = []
    for library_book in library_books:
      if library_book.library.libraryUid == library_uid:
        if library_book.availableCount != 0 or show_all == True:
          library_book_items.append(
            LibraryBookResponse(
              name=library_book.book.name,
              author=library_book.book.author,
              genre=library_book.book.genre,
              condition=library_book.book.condition,
              bookUid=library_book.book.bookUid,
              availableCount=library_book.availableCount,
            )
          )

    return LibraryBookPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=len(library_book_items),
      items=library_book_items[(page - 1) * size : page * size]
    )
  
  
  async def get_user_rented_books(
      self,
      X_User_Name: str,
      page: int = 1,
      size: int = 100,
  ):
    reservations: list[Reservation] = await self._reservationCRUD.get_all_reservations(
      page=page,
      size=size,
      username=X_User_Name,
    )

    book_reservations: list[BookReservationResponse] = []
    for reservation in reservations:
      try:
        library: LibraryResponse = await self._libraryCRUD.get_library_by_uid(reservation.libraryUid)
        book: BookInfo = await self._libraryCRUD.get_book_by_uid(reservation.bookUid)

        book_reservations.append(
          BookReservationResponse(
            reservationUid=reservation.reservationUid,
            username=reservation.username,
            status=reservation.status,
            startDate=reservation.startDate,
            tillDate=reservation.tillDate,
            library=library,
            book=book,
          )
        )
      except ServiceUnavailableException:
        book_reservations.append(
          BookReservationResponse(
            reservationUid=reservation.reservationUid,
            username=reservation.username,
            status=reservation.status,
            startDate=reservation.startDate,
            tillDate=reservation.tillDate,
            library=LibraryResponse(
              libraryUid=reservation.libraryUid,
              name=None,
              city=None,
              address=None,
            ),
            book=BookInfo(
              bookUid=reservation.bookUid,
              name=None,
              author=None,
              genre=None,
              condition=None,
            ),
          )
        )

    return book_reservations
  

  async def get_user_rating(
      self,
      X_User_Name: str,
  ):
    rating = await self.__get_rating_by_username(
      username=X_User_Name
    )
    return UserRatingResponse(
      stars= rating.stars,
    )
  

  async def take_book(
      self,
      X_User_Name: str,
      take_book_request: TakeBookRequest,
  ):
    user_rented_books = await self._reservationCRUD.get_all_reservations(
      size=sys.maxsize,
      username=X_User_Name,
      status=ReservationStatus.RENTED,
    )
    user_rating = await self.get_user_rating(
      X_User_Name=X_User_Name,
    )

    if (len(user_rented_books) >= user_rating.stars):
      raise BadRequestException(prefix="take_book")
    
    library_book = await self.__get_book_in_library(
      libraryUid=take_book_request.libraryUid,
      bookUid=take_book_request.bookUid,
    )

    if (library_book.availableCount == 0):
      raise BadRequestException(prefix="take_book")
    
    reservation_uid = await self._reservationCRUD.add_reservation(
      ReservationCreate(
        username=X_User_Name,
        library_uid=take_book_request.libraryUid,
        book_uid=take_book_request.bookUid,
        status=ReservationStatus.RENTED,
        start_date=datetime.now().strftime('%Y-%m-%d'),
        till_date=take_book_request.tillDate.strftime('%Y-%m-%d'),
      )
    )

    reservation = await self._reservationCRUD.get_reservation_by_uid(
      uid=reservation_uid,
    )

    try:
      await self._libraryCRUD.patch_library_book(
        id=library_book.id,
        update=LibraryBookUpdate(
          available_count=library_book.availableCount - 1,
        ),
      )
    except ServiceUnavailableException:
      await self._reservationCRUD.delete_reservation(reservation)

    return TakeBookResponse(
      reservationUid=reservation.reservationUid,
      status=reservation.status,
      startDate=reservation.startDate,
      tillDate=reservation.tillDate,
      library=library_book.library,
      book=library_book.book,
      rating=user_rating,
    )
  

  async def return_book(
    self,
    X_User_Name: str,
    reservation_uid: UUID,
    return_book_request: ReturnBookRequest,
  ):
    reservation: Reservation = await self._reservationCRUD.get_reservation_by_uid(
      uid=reservation_uid
    )
    if not reservation:
      raise NotFoundException(prefix="return_book", message="Бронирование не найдено")
    
    status_return = await self.__change_reservation_info(
      reservation=reservation,
      return_book_request=return_book_request
    )
    
    try:
      book = await self._libraryCRUD.get_book_by_uid(
        uid=reservation.bookUid,
      )

      await self._libraryCRUD.patch_book( # upd book condition
        uid=reservation.bookUid,
        update=BookUpdate(
          condition=return_book_request.condition,
        )
      )

      library_book = await self.__get_book_in_library( # find library_book info
        libraryUid=reservation.libraryUid,
        bookUid=reservation.bookUid,
      )

      await self._libraryCRUD.patch_library_book( # inc available count
        id=library_book.id,
        update=LibraryBookUpdate(
          available_count=library_book.availableCount + 1,
        ),
      )
    except ServiceUnavailableException:
      RequestQueue.add_http_request(
        url=f'{self.http_path}reservations/{reservation_uid}/return',
        headers={"X-User-Name": X_User_Name},
        data=return_book_request.model_dump(mode='json'),
        http_method=requests.post,
      )

    try:
      await self.__change_user_rating(
        X_User_Name=X_User_Name,
        status_return=status_return,
        updated_condition=return_book_request.condition,
        book_condtiton=book.condition,
      )
    except ServiceUnavailableException:
      RequestQueue.add_http_request(
        url=f'{self.http_path}reservations/{reservation_uid}/return',
        headers={"X-User-Name": X_User_Name},
        data=return_book_request.model_dump(mode='json'),
        http_method=requests.post,
      )

    return None


  async def __change_user_rating(
      self,
      X_User_Name: str,
      status_return: ReservationStatus,
      updated_condition: ConditionStatus,
      book_condtiton: ConditionStatus,
  ) -> None:
    rating = await self.__get_rating_by_username(
      username=X_User_Name,
    )

    stars = rating.stars
    okFlag = True

    if (status_return == ReservationStatus.EXPIRED):
      stars -= 10
      okFlag = False
    
    if (book_condtiton != updated_condition):
      stars -= 10
      okFlag = False

    if (okFlag):
      stars += 1

    if (stars < 1):
      stars = 0
    elif (stars > 100):
      stars = 100

    await self._ratingCRUD.patch_rating(
      id=rating.id,
      update=RatingUpdate(
        stars=stars,
      )
    )
    

  async def __change_reservation_info(
      self,
      reservation: Reservation,
      return_book_request: ReturnBookRequest,
  ) -> ReservationStatus:
    status_return = ReservationStatus.RETURNED \
      if return_book_request.date <= reservation.tillDate \
      else ReservationStatus.EXPIRED
    
    await self._reservationCRUD.patch_reservation(
      uid=reservation.reservationUid,
      update=ReservationUpdate(
        status=status_return,
      )
    )

    return status_return
    

  async def __get_book_in_library(
      self,
      libraryUid: UUID,
      bookUid: UUID,
  ) -> LibraryBookEntityResponse:
    library_books = await self._libraryCRUD.get_all_library_books(
      size=sys.maxsize,
    )

    library_book_items: list[LibraryBookEntityResponse] = []
    for library_book in library_books:
      if library_book.book.bookUid == bookUid and library_book.library.libraryUid == libraryUid:
        library_book_items.append(
          library_book,
        )

    if len(library_book_items) > 1:
      raise BadRequestException(prefix="__get_book_in_library")
    elif len(library_book_items) == 0:
      raise NotFoundException(prefix="__get_book_in_library")
    else:
      return library_book_items[0]
    

  async def __get_rating_by_username(
      self,
      username: str,
  ) -> Rating:
    ratings: list[Rating] = await self._ratingCRUD.get_all_ratings(
      username=username,
    )
    
    if ratings:
      if len(ratings) > 1:
        raise BadRequestException(prefix="get_rating_by_username")
    
      return ratings[0]
    else:
      rating_id = await self._ratingCRUD.add_rating(RatingCreate(
        username=username,
        stars=50,
      ))

      rating = await self._ratingCRUD.get_rating_by_id(
        id=rating_id,
      )

      return rating
