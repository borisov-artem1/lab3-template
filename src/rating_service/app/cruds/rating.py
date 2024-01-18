from sqlalchemy.orm import Session, Query

from schemas.rating import RatingFilter, RatingUpdate
from models.rating import RatingModel


class RatingCRUD():
  def __init__(self, db: Session):
    self._db = db

  async def get_all(
      self,
      filter: RatingFilter,
      offset: int = 0,
      limit: int = 100,
  ) -> list[RatingModel]:
    ratings = self._db.query(RatingModel)
    ratings = await self.__filter_ratings(ratings, filter)
    return ratings.offset(offset).limit(limit).all()
  
  async def get_by_id(self, id: int) -> RatingModel | None:
    return self._db.query(RatingModel).filter(RatingModel.id == id).first()
  
  async def create(self, rating: RatingModel) -> RatingModel | None:
    try:
      self._db.add(rating)
      self._db.commit()
      self._db.refresh(rating)
    except:
      return None
    
    return rating
  
  async def update(self, rating: RatingModel, rating_update: RatingUpdate) -> RatingModel | None:
    update_fields = rating_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
      setattr(rating, key, value)

    try:
      self._db.add(rating)
      self._db.commit()
      self._db.refresh(rating)
    except:
      return None
    
    return rating
  
  async def delete(self, rating: RatingModel) -> RatingModel:
    self._db.delete(rating)
    self._db.commit()

    return rating

  async def __filter_ratings(
      self,
      ratings: Query[RatingModel],
      filter: RatingFilter
    ) -> Query[RatingModel]:
    if filter.username:
      ratings = ratings.filter(RatingModel.username == filter.username)

    if filter.stars:
      ratings = ratings.filter(RatingModel.stars == filter.stars)

    return ratings
