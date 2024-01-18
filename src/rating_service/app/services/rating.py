from sqlalchemy.orm import Session

from cruds.rating import RatingCRUD
from schemas.rating import RatingFilter, RatingUpdate, RatingCreate
from exceptions.http import NotFoundException, ConflictException
from models.rating import RatingModel


class RatingService():
  def __init__(self, ratingCRUD: RatingCRUD, db: Session):
    self._ratingCRUD: RatingCRUD = ratingCRUD(db)

  async def get_all(
      self,
      filter: RatingFilter,
      page: int = 1,
      size: int = 100,
  ):
    return await self._ratingCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
  
  async def get_by_id(
      self, 
      id: int,
  ):
    rating = await self._ratingCRUD.get_by_id(id)
    if rating is None:
      raise NotFoundException(prefix="get rating")
    
    return rating

  async def create(
      self,
      rating_create: RatingCreate,
  ):
    rating = RatingModel(**rating_create.model_dump())
    rating = await self._ratingCRUD.create(rating)
    if rating is None:
      raise ConflictException(prefix="create rating")
    
    return rating
  
  async def patch(
      self,
      id: int,
      rating_patch: RatingUpdate,
  ):
    rating = await self._ratingCRUD.get_by_id(id)
    if rating is None:
      raise NotFoundException(prefix="patch rating")
    
    rating = await self._ratingCRUD.update(rating, rating_patch)
    if rating is None:
      raise ConflictException(prefix="patch rating")
    
    return rating
  
  async def delete(
      self,
      id: int,
  ):
    rating = await self._ratingCRUD.get_by_id(id)
    if rating is None:
      raise NotFoundException(prefix="delete rating")
    
    return await self._ratingCRUD.delete(rating)
