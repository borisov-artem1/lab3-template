from models.rating import RatingModel
from schemas.rating import RatingFilter
from cruds.mocks.data import RatingMockData


class RatingMockCRUD(RatingMockData):
  def __init__(self, db):
        self._db = db
        
  async def get_all(
      self,
      filter: RatingFilter,
      offset: int = 0,
      limit: int = 100
    ):
    
    ratings = [
      RatingModel(**item) for item in self._ratings
    ]
    ratings = await self.__filter_ratings(ratings, filter)
  
    return ratings[offset:limit]
  
  async def get_by_id(self, rating_id: int):
    for item in self._ratings:
      if item["id"] == rating_id:
        return RatingModel(**item)
      
    return None
  
  async def create(self, rating: RatingModel):  
    self._ratings.append(
      {
        "id": 1 if len(self._ratings) == 0 
            else self._ratings[-1]["id"] + 1,
        "username": rating.username,
        "stars": rating.stars,
      },
    )
    
    return RatingModel(**self._ratings[-1])

  async def delete(self, rating: RatingModel):
    for i in range(len(self._ratings)):
      item = self._ratings[i]
      if item["id"] == rating.id:
        deleted_rating = self._ratings.pop(i)
        break

    return RatingModel(**deleted_rating)
  
  async def __filter_ratings(self, ratings, rating_filter: RatingFilter):
    return ratings
