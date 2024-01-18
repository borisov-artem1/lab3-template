from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from datetime import datetime as dt

from cruds.reservation import ReservationCRUD
from enums.responses import RespReservationEnum
from schemas.reservation import Reservation, ReservationFilter, ReservationCreate, ReservationUpdate
from utils.database import get_db
from services.reservation import ReservationService
from enums.status import ReservationStatus


def get_reservation_crud() -> ReservationCRUD:
  return ReservationCRUD


router = APIRouter(
  prefix="/reservation",
  tags=["Reservation REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespReservationEnum.InvaluidData.value,
  },
)


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=list[Reservation],
  responses={
    status.HTTP_200_OK: RespReservationEnum.GetAll.value,
  }
)
async def get_all_reservation(
  db: Annotated[Session, Depends(get_db)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  username: Annotated[str | None, Query(max_length=800)] = None,
  book_uuid: UUID | None = None,
  library_uuid: UUID | None = None,
  status: ReservationStatus | None = None,
  start_date: dt | None = None,
  till_date: dt | None = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
):
  return await ReservationService(
    reservationCRUD=reservationCRUD,
    db=db,
  ).get_all(
      filter=ReservationFilter(
        username=username,
        book_uuid=book_uuid,
        library_uuid=library_uuid,
        status=status,
        start_date=start_date,
        till_date=till_date,
      ),
      page=page,
      size=size,
    )


@router.get(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Reservation,
  responses={
    status.HTTP_200_OK: RespReservationEnum.GetByUID.value,
    status.HTTP_404_NOT_FOUND: RespReservationEnum.NotFound.value,
  },
)
async def get_reservation_by_uid(
  db: Annotated[Session, Depends(get_db)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  uid: UUID,
):
  return await ReservationService(
    reservationCRUD=reservationCRUD,
    db=db,
  ).get_by_uid(
    uid=uid,
  )


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: RespReservationEnum.Created.value,
  },
)
async def create_reservation(
  db: Annotated[Session, Depends(get_db)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  reservation_create: ReservationCreate,
):
  reservation = await ReservationService(
    reservationCRUD=reservationCRUD,
    db=db,
  ).create(
    reservation_create=reservation_create,
  )

  return Response(
    status_code=status.HTTP_201_CREATED,
    headers={"Location": f"/api/v1/reservation/{reservation.reservation_uid}"}
  )


@router.patch(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Reservation,
  responses={
    status.HTTP_200_OK: RespReservationEnum.Patch.value,
    status.HTTP_404_NOT_FOUND: RespReservationEnum.NotFound.value,
  },
)
async def update_reservation(
  db: Annotated[Session, Depends(get_db)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  uid: UUID,
  reservation_update: ReservationUpdate,
):
  return await ReservationService(
    reservationCRUD=reservationCRUD,
    db=db,
  ).patch(
    uid=uid,
    reservation_patch=reservation_update,
  )


@router.delete(
  "/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: RespReservationEnum.Delete.value,
    status.HTTP_404_NOT_FOUND: RespReservationEnum.NotFound.value,
  },
)
async def delete_reservation(
  db: Annotated[Session, Depends(get_db)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  uid: UUID,
):
  await ReservationService(
    reservationCRUD=reservationCRUD,
    db=db,
  ).delete(
    uid=uid,
  )

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
  )
