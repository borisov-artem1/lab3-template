from copy import deepcopy
from datetime import datetime as dt

from cruds.mocks.rating import RatingMockCRUD
from cruds.mocks.data import RatingMockData
from services.rating import RatingService
from schemas.rating import RatingFilter, RatingCreate
from models.rating import RatingModel
from exceptions.http import NotFoundException, ConflictException


ratingService = RatingService(
  ratingCRUD=RatingMockCRUD,
  db=None,
)
correct_ratings = deepcopy(RatingMockData._ratings)


def model_into_dict(model: RatingModel) -> dict:
  dictionary = model.__dict__
  del dictionary["_sa_instance_state"]
  return dictionary


async def test_get_all_ratings_success():
  try:
    ratings = await ratingService.get_all(
      filter=RatingFilter()
    )

    assert len(ratings) == len(correct_ratings)
    for i in range(len(ratings)):
      assert model_into_dict(ratings[i]) == correct_ratings[i]
  except:
    assert False


async def test_get_rating_by_id_success():
  try:
    rating = await ratingService.get_by_id(1)

    assert model_into_dict(rating) == correct_ratings[0]
  except:
    assert False


async def test_get_rating_by_id_not_found():
  try:
    await ratingService.get_by_id(10)

    assert False
  except NotFoundException:
    assert True
  except:
    assert False


async def test_add_rating_success():
  try:
    rating = await ratingService.create(
      RatingCreate(
        username="test",
        stars=23,
      )
    )
    
    assert \
      rating.username == "test" and \
      rating.stars == 23
  except:
    assert False

async def test_delete_rating_success():
  try:
    rating = await ratingService.delete(3)

    assert correct_ratings[2] == model_into_dict(rating)
  except:
    assert False


async def test_delete_rating_not_found():
  try:
    await ratingService.delete(10)
    
    assert False
  except NotFoundException:
    assert True
  except:
    assert False
