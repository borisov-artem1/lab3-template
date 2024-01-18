from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from cruds.library import LibraryCRUD
from enums.responses import RespLibraryEnum
from schemas.library import Library, LibraryFilter, LibraryCreate, LibraryUpdate, LibraryPaginationResponse
from utils.database import get_db
from services.library import LibraryService


def get_library_crud() -> LibraryCRUD:
  return LibraryCRUD


router = APIRouter(
  prefix="/library",
  tags=["Library REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespLibraryEnum.InvalidData.value,
  },
)


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=LibraryPaginationResponse,
  responses={
    status.HTTP_200_OK: RespLibraryEnum.GetAll.value,
  }
)
async def get_all_library(
  db: Annotated[Session, Depends(get_db)],
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  name: Annotated[str | None, Query(max_length=80)] = None,
  city: Annotated[str | None, Query(max_length=255)] = None,
  address: Annotated[str | None, Query(max_length=255)] = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
):
  return await LibraryService(
    libraryCRUD=libraryCRUD,
    db=db,
  ).get_all(
      filter=LibraryFilter(
        name=name,
        city=city,
        address=address,
      ),
      page=page,
      size=size,
    )


@router.get(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Library,
  responses={
    status.HTTP_200_OK: RespLibraryEnum.GetByUID.value,
    status.HTTP_404_NOT_FOUND: RespLibraryEnum.NotFound.value,
  },
)
async def get_library_by_uid(
  db: Annotated[Session, Depends(get_db)],
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  uid: UUID,
):
  return await LibraryService(
    libraryCRUD=libraryCRUD,
    db=db,
  ).get_by_uid(
    uid=uid,
  )


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: RespLibraryEnum.Created.value,
  },
)
async def create_library(
  db: Annotated[Session, Depends(get_db)],
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  library_create: LibraryCreate,
):
  library = await LibraryService(
    libraryCRUD=libraryCRUD,
    db=db,
  ).create(
    library_create=library_create,
  )

  return Response(
    status_code=status.HTTP_201_CREATED,
    headers={"Location": f"/api/v1/library/{library.library_uid}"}
  )


@router.patch(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Library,
  responses={
    status.HTTP_200_OK: RespLibraryEnum.Patch.value,
    status.HTTP_404_NOT_FOUND: RespLibraryEnum.NotFound.value,
  },
)
async def update_library(
  db: Annotated[Session, Depends(get_db)],
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  uid: UUID,
  library_update: LibraryUpdate,
):
  return await LibraryService(
    libraryCRUD=libraryCRUD,
    db=db,
  ).patch(
    uid=uid,
    library_patch=library_update,
  )


@router.delete(
  "/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: RespLibraryEnum.Delete.value,
    status.HTTP_404_NOT_FOUND: RespLibraryEnum.NotFound.value,
  },
)
async def delete_library(
  db: Annotated[Session, Depends(get_db)],
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  uid: UUID,
):
  await LibraryService(
    libraryCRUD=libraryCRUD,
    db=db,
  ).delete(
    uid=uid,
  )

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
  )
