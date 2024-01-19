import json
from uuid import UUID
import requests
from requests import Response
from fastapi import status

from cruds.base import BaseCRUD
from utils.settings import get_settings
from utils.circuit_breaker import CircuitBreaker
from schemas.rating import Rating, RatingUpdate, RatingCreate
from exceptions.http import ServiceUnavailableException


class RatingCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    rating_host = settings["services"]["gateway"]["rating_host"]
    rating_port = settings["services"]["rating"]["port"]

    self.http_path = f'http://{rating_host}:{rating_port}/api/v1/'

  async def get_all_ratings(
      self,
      page: int = 1,
      size: int = 100,
      username: str | None = None,
  ):
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}rating/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}',
      http_method=requests.get,
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating_json: list[Rating] = response.json()

    ratings: list[Rating] = []
    for rating in rating_json:
      ratings.append(
        Rating(
          id=rating["id"],
          username=rating["username"],
          stars=rating["stars"],
        )
      )
    
    return ratings
  

  async def get_rating_by_id(
      self,
      id: int,
  ) -> Rating:
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}rating/{id}',
      http_method=requests.get,
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating_json = response.json()

    return Rating(
      id=rating_json["id"],
      username=rating_json["username"],
      stars=rating_json["stars"],
    )
  

  async def add_rating(
      self,
      create: RatingCreate,
  ) -> int:
    try:
      response: Response = requests.post(
        url=f'{self.http_path}rating/',
        data=json.dumps(create.model_dump())
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    location: str = response.headers["location"]
    id = str(location.split("/")[-1])

    return id
  

  async def patch_rating(
      self,
      id: int,
      update: RatingUpdate,
  ):
    try:
      response: Response = requests.patch(
        url=f'{self.http_path}rating/{id}',
        data=json.dumps(update.model_dump(exclude_unset=True))
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating = response.json()
    return rating["id"]
