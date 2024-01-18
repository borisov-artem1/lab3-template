from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from cruds.rating import RatingCRUD
from enums.responses import RespRatingEnum
from schemas.rating import Rating, RatingFilter, RatingCreate, RatingUpdate
from utils.database import get_db
from services.rating import RatingService


def get_rating_crud() -> RatingCRUD:
  return RatingCRUD


router = APIRouter(
  prefix="/rating",
  tags=["Rating REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespRatingEnum.InvalidData.value,
  },
)


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=list[Rating],
  responses={
    status.HTTP_200_OK: RespRatingEnum.GetAll.value,
  }
)
async def get_all_rating(
  db: Annotated[Session, Depends(get_db)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
  username: Annotated[str | None, Query(max_length=800)] = None,
  stars: Annotated[int | None, Query(ge=1,le=100)] = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
):
  return await RatingService(
    ratingCRUD=ratingCRUD,
    db=db,
  ).get_all(
      filter=RatingFilter(
        username=username,
        stars=stars,
      ),
      page=page,
      size=size,
    )


@router.get(
  "/{id}",
  status_code=status.HTTP_200_OK,
  response_model=Rating,
  responses={
    status.HTTP_200_OK: RespRatingEnum.GetByUID.value,
    status.HTTP_404_NOT_FOUND: RespRatingEnum.NotFound.value,
  },
)
async def get_rating_by_id(
  db: Annotated[Session, Depends(get_db)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
  id: int,
):
  return await RatingService(
    ratingCRUD=ratingCRUD,
    db=db,
  ).get_by_id(
    id=id,
  )


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: RespRatingEnum.Created.value,
  },
)
async def create_rating(
  db: Annotated[Session, Depends(get_db)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
  rating_create: RatingCreate,
):
  rating = await RatingService(
    ratingCRUD=ratingCRUD,
    db=db,
  ).create(
    rating_create=rating_create,
  )

  return Response(
    status_code=status.HTTP_201_CREATED,
    headers={"Location": f"/api/v1/rating/{rating.id}"}
  )


@router.patch(
  "/{id}",
  status_code=status.HTTP_200_OK,
  response_model=Rating,
  responses={
    status.HTTP_200_OK: RespRatingEnum.Patch.value,
    status.HTTP_404_NOT_FOUND: RespRatingEnum.NotFound.value,
  },
)
async def update_rating(
  db: Annotated[Session, Depends(get_db)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
  id: int,
  rating_update: RatingUpdate,
):
  return await RatingService(
    ratingCRUD=ratingCRUD,
    db=db,
  ).patch(
    id=id,
    rating_patch=rating_update,
  )


@router.delete(
  "/{id}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: RespRatingEnum.Delete.value,
    status.HTTP_404_NOT_FOUND: RespRatingEnum.NotFound.value,
  },
)
async def delete_rating(
  db: Annotated[Session, Depends(get_db)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
  id: int,
):
  await RatingService(
    ratingCRUD=ratingCRUD,
    db=db,
  ).delete(
    id=id,
  )

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
  )
