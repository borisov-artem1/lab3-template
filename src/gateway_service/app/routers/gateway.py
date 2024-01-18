from fastapi import APIRouter, Depends, status, Query, Header
from fastapi.responses import Response
from typing import Annotated
from uuid import UUID


from cruds.library import LibraryCRUD
from cruds.reservation import ReservationCRUD 
from cruds.rating import RatingCRUD
from enums.responses import RespEnum
from schemas.library import (
  LibraryPaginationResponse,
  LibraryBookPaginationResponse,
)
from schemas.reservation import (
  BookReservationResponse,
  TakeBookRequest,
  TakeBookResponse,
  ReturnBookRequest,
)
from schemas.rating import (
  UserRatingResponse,
)
from services.gateway import GatewayService


def get_library_crud() -> LibraryCRUD:
  return LibraryCRUD

def get_reservation_crud() -> ReservationCRUD:
  return ReservationCRUD

def get_rating_crud() -> RatingCRUD:
  return RatingCRUD


router = APIRouter(
  tags=["Gateway API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespEnum.InvalidData.value,
  }
)


@router.get(
  "/libraries", 
  status_code=status.HTTP_200_OK,
  response_model=LibraryPaginationResponse,
  responses={
    status.HTTP_200_OK: RespEnum.GetAllLibraries.value,
  }
)
async def get_list_of_libraries(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    city: Annotated[str, Query(max_length=80)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).get_all_libraries_in_city(
      city=city,
      page=page,
      size=size
    )


@router.get(
  "/libraries/{libraryUid}/books",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBookPaginationResponse,
  responses={
    status.HTTP_200_OK: RespEnum.GetAllBooksInLibrary.value,
  }
)
async def get_books_in_library(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    libraryUid: UUID,
    showAll: bool = False,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).get_books_in_library(
      library_uid=libraryUid,
      show_all=showAll,
      page=page,
      size=size
    )


@router.get(
  "/reservations",
  status_code=status.HTTP_200_OK,
  response_model=list[BookReservationResponse],
  responses={
    status.HTTP_200_OK: RespEnum.GetUserRentedBooks.value,
  }
)
async def get_user_rented_books(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).get_user_rented_books(
      X_User_Name=X_User_Name,
      page=page,
      size=size
    )


@router.get(
  "/rating",
  status_code=status.HTTP_200_OK,
  response_model=UserRatingResponse,
  responses={
    status.HTTP_200_OK: RespEnum.GetUserRating.value,
  }
)
async def get_user_rating(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)],
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).get_user_rating(
      X_User_Name=X_User_Name,
    )


@router.post(
  "/reservations",
  status_code=status.HTTP_200_OK,
  response_model=TakeBookResponse,
  responses={
    status.HTTP_200_OK: RespEnum.TakeBook.value,
  }
)
async def take_book(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)],
    take_book_request: TakeBookRequest,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).take_book(
      X_User_Name=X_User_Name,
      take_book_request=take_book_request,
    )


@router.post(
  "/reservations/{reservationUid}/return",
  status_code=status.HTTP_204_NO_CONTENT,
  response_model=None,
  responses={
    status.HTTP_204_NO_CONTENT: RespEnum.ReturnBook.value,
    status.HTTP_404_NOT_FOUND: RespEnum.ReservationNotFound.value,
  }
)
async def return_book(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
    ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)],
    reservationUid: UUID,
    retutn_book_request: ReturnBookRequest,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD,
      reservationCRUD=reservationCRUD,
      ratingCRUD=ratingCRUD,
    ).return_book(
      X_User_Name=X_User_Name,
      reservation_uid=reservationUid,
      return_book_request=retutn_book_request
    )
