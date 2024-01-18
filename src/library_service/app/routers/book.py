from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from cruds.book import BookCRUD
from enums.responses import RespBookEnum
from enums.status import ConditionStatus
from schemas.book import Book, BookFilter, BookCreate, BookUpdate
from utils.database import get_db
from services.book import BookService


def get_book_crud() -> BookCRUD:
  return BookCRUD


router = APIRouter(
  prefix="/book",
  tags=["Book REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespBookEnum.InvalidData.value,
  },
)


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=list[Book],
  responses={
    status.HTTP_200_OK: RespBookEnum.GetAll.value,
  }
)
async def get_all_book(
  db: Annotated[Session, Depends(get_db)],
  bookCRUD: Annotated[BookCRUD, Depends(get_book_crud)],
  name: Annotated[str | None, Query(max_length=255)] = None,
  author: Annotated[str | None, Query(max_length=255)] = None,
  genre: Annotated[str | None, Query(max_length=255)] = None,
  condition: ConditionStatus | None = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
):
  return await BookService(
    bookCRUD=bookCRUD,
    db=db,
  ).get_all(
      filter=BookFilter(
        name=name,
        author=author,
        genre=genre,
        condition=condition,
      ),
      page=page,
      size=size,
    )


@router.get(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Book,
  responses={
    status.HTTP_200_OK: RespBookEnum.GetByUID.value,
    status.HTTP_404_NOT_FOUND: RespBookEnum.NotFound.value,
  },
)
async def get_book_by_uid(
  db: Annotated[Session, Depends(get_db)],
  bookCRUD: Annotated[BookCRUD, Depends(get_book_crud)],
  uid: UUID,
):
  return await BookService(
    bookCRUD=bookCRUD,
    db=db,
  ).get_by_uid(
    uid=uid,
  )


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: RespBookEnum.Created.value,
  },
)
async def create_book(
  db: Annotated[Session, Depends(get_db)],
  bookCRUD: Annotated[BookCRUD, Depends(get_book_crud)],
  book_create: BookCreate,
):
  book = await BookService(
    bookCRUD=bookCRUD,
    db=db,
  ).create(
    book_create=book_create,
  )

  return Response(
    status_code=status.HTTP_201_CREATED,
    headers={"Location": f"/api/v1/book/{book.book_uid}"}
  )


@router.patch(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Book,
  responses={
    status.HTTP_200_OK: RespBookEnum.Patch.value,
    status.HTTP_404_NOT_FOUND: RespBookEnum.NotFound.value,
  },
)
async def update_book(
  db: Annotated[Session, Depends(get_db)],
  bookCRUD: Annotated[BookCRUD, Depends(get_book_crud)],
  uid: UUID,
  book_update: BookUpdate,
):
  return await BookService(
    bookCRUD=bookCRUD,
    db=db,
  ).patch(
    uid=uid,
    book_patch=book_update,
  )


@router.delete(
  "/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: RespBookEnum.Delete.value,
    status.HTTP_404_NOT_FOUND: RespBookEnum.NotFound.value,
  },
)
async def delete_book(
  db: Annotated[Session, Depends(get_db)],
  bookCRUD: Annotated[BookCRUD, Depends(get_book_crud)],
  uid: UUID,
):
  await BookService(
    bookCRUD=bookCRUD,
    db=db,
  ).delete(
    uid=uid,
  )

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
  )
